"""Post and channel media downloader engine."""

from __future__ import annotations
import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union, List, Dict, Any, Callable
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.custom.message import Message

logger = logging.getLogger(__name__)


@dataclass
class PostDownloadResult:
    message_id: int
    peer: Union[str, int]
    media_path: Optional[str]
    metadata_path: Optional[str]
    caption: str
    uploaded_date: str
    media_type: str
    success: bool
    error: Optional[str] = None


def format_post_metadata(
    peer: Union[str, int],
    message_id: int,
    caption: str,
    date: datetime,
    media_type: str,
    views: Optional[int] = None,
    forwards: Optional[int] = None,
    edit_date: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Format post metadata into standardized dictionary."""
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    return {
        "peer": str(peer),
        "message_id": message_id,
        "caption": caption or "",
        "uploaded_date": date.isoformat(),
        "media_type": media_type,
        "views": views,
        "forwards": forwards,
        "edit_date": edit_date.isoformat() if edit_date else None,
    }


def build_output_filepath(
    base_dir: Path,
    category: str,
    peer: Union[str, int],
    item_id: int,
    filename: str,
) -> Path:
    """Build clean output path for downloaded items."""
    clean_peer = str(peer).replace("/", "_").replace("\\", "_")
    target_dir = base_dir / category / clean_peer
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f"{item_id}_{filename}"


def detect_media_type(message: Message) -> str:
    """Detect whether message media is photo, video, document, audio, etc."""
    if message.photo:
        return "photo"
    if message.video:
        return "video"
    if message.audio:
        return "audio"
    if message.voice:
        return "voice"
    if message.document:
        # Check mime_type or file extension
        mime = getattr(message.document, "mime_type", "")
        if "video" in mime:
            return "video"
        if "image" in mime:
            return "photo"
        return "document"
    return "unknown"


async def download_single_post(
    client: TelegramClient,
    peer: Union[str, int],
    message_id: int,
    base_dir: Path,
) -> PostDownloadResult:
    """Download a specific post's video or photo, caption, and uploaded date."""
    target_dir = base_dir / "posts" / str(peer)
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        message = await client.get_messages(peer, ids=message_id)
        if not message:
            return PostDownloadResult(
                message_id=message_id,
                peer=peer,
                media_path=None,
                metadata_path=None,
                caption="",
                uploaded_date="",
                media_type="none",
                success=False,
                error=f"Message {message_id} not found in peer {peer}.",
            )

        caption = message.message or message.text or ""
        post_date = message.date
        media_type = detect_media_type(message) if message.media else "none"

        downloaded_file = None
        if message.media:
            prefix = f"{message_id}_media"
            target_path = target_dir / prefix
            downloaded_file = await client.download_media(
                message,
                file=str(target_path),
            )

        metadata = format_post_metadata(
            peer=peer,
            message_id=message_id,
            caption=caption,
            date=post_date,
            media_type=media_type,
            views=message.views,
            forwards=message.forwards,
            edit_date=message.edit_date,
        )
        if downloaded_file:
            metadata["saved_file"] = str(downloaded_file)

        meta_path = target_dir / f"{message_id}_metadata.json"
        meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

        return PostDownloadResult(
            message_id=message_id,
            peer=peer,
            media_path=str(downloaded_file) if downloaded_file else None,
            metadata_path=str(meta_path),
            caption=caption,
            uploaded_date=metadata["uploaded_date"],
            media_type=media_type,
            success=True,
        )

    except FloodWaitError as e:
        logger.warning(f"Flood wait error: must wait {e.seconds}s")
        await asyncio.sleep(e.seconds)
        return await download_single_post(client, peer, message_id, base_dir)
    except Exception as e:
        logger.error(f"Error downloading post {message_id} from {peer}: {e}")
        return PostDownloadResult(
            message_id=message_id,
            peer=peer,
            media_path=None,
            metadata_path=None,
            caption="",
            uploaded_date="",
            media_type="none",
            success=False,
            error=str(e),
        )


async def download_channel_posts(
    client: TelegramClient,
    peer: Union[str, int],
    base_dir: Path,
    limit: Optional[int] = None,
    media_only: bool = True,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> List[PostDownloadResult]:
    """Iterate and download all (or up to limit) posts from a channel."""
    results: List[PostDownloadResult] = []
    count = 0

    async for msg in client.iter_messages(peer, limit=limit):
        if media_only and not msg.media:
            continue
        res = await download_single_post(client, peer, msg.id, base_dir)
        results.append(res)
        count += 1
        if progress_callback:
            progress_callback(count, limit or count)
        # Gentle rate limit pause
        await asyncio.sleep(0.1)

    return results
