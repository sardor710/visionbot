"""Story downloading logic with 24-hour and all-time filtering."""

from __future__ import annotations
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Optional, Union, Any, Callable
from telethon import TelegramClient
from telethon.tl.functions.stories import GetPeerStoriesRequest, GetStoriesByIDRequest
from telethon.tl.types import StoryItem, PeerUser, PeerChannel
from telebot_downloader.core.parser import StoryFilterMode

logger = logging.getLogger(__name__)


@dataclass
class MockStory:
    """Mock story model for testing and offline simulation."""
    story_id: int
    date: datetime
    caption: str = ""
    media_type: str = "photo"
    media: Any = None


@dataclass
class StoryDownloadResult:
    story_id: int
    peer: Union[str, int]
    media_path: Optional[str]
    metadata_path: Optional[str]
    caption: str
    uploaded_date: str
    media_type: str
    success: bool
    error: Optional[str] = None


def filter_stories_by_mode(
    stories: List[Any],
    mode: StoryFilterMode,
    current_time: Optional[datetime] = None,
) -> List[Any]:
    """Filter stories list based on ALL or LAST_24_HOURS mode."""
    if mode == StoryFilterMode.ALL:
        return stories

    if current_time is None:
        current_time = datetime.now(timezone.utc)
    elif current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)

    cutoff = current_time - timedelta(hours=24)
    filtered = []
    for s in stories:
        s_date = getattr(s, "date", None)
        if s_date:
            if s_date.tzinfo is None:
                s_date = s_date.replace(tzinfo=timezone.utc)
            if s_date >= cutoff:
                filtered.append(s)
    return filtered


def get_story_caption(story: Any) -> str:
    """Extract caption string from story item."""
    if hasattr(story, "caption") and story.caption:
        return story.caption
    if hasattr(story, "message") and story.message:
        return story.message
    return ""


def get_story_date(story: Any) -> datetime:
    """Extract story date with UTC timezone."""
    d = getattr(story, "date", datetime.now(timezone.utc))
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d


async def fetch_peer_stories(client: TelegramClient, peer: Union[str, int]) -> List[Any]:
    """Fetch stories of a given peer (user or channel) via Telethon MTProto."""
    entity = await client.get_input_entity(peer)
    result = await client(GetPeerStoriesRequest(peer=entity))
    if hasattr(result, "stories") and hasattr(result.stories, "stories"):
        return [s for s in result.stories.stories if isinstance(s, StoryItem)]
    return []


async def download_single_story(
    client: TelegramClient,
    peer: Union[str, int],
    story_id: int,
    base_dir: Path,
) -> StoryDownloadResult:
    """Download a single story by ID with its caption and date metadata."""
    out_dir = base_dir / "stories" / str(peer)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        entity = await client.get_input_entity(peer)
        result = await client(GetStoriesByIDRequest(peer=entity, id=[story_id]))
        stories = result.stories if hasattr(result, "stories") else []
        if not stories:
            return StoryDownloadResult(
                story_id=story_id,
                peer=peer,
                media_path=None,
                metadata_path=None,
                caption="",
                uploaded_date="",
                media_type="unknown",
                success=False,
                error=f"Story {story_id} not found or expired.",
            )

        story = stories[0]
        caption = get_story_caption(story)
        date = get_story_date(story)
        uploaded_date_iso = date.isoformat()

        # Determine media filename
        media_type = "video" if getattr(story, "media", None) and hasattr(story.media, "document") else "photo"
        target_file_prefix = f"story_{story_id}"
        
        # Download media
        downloaded_file = await client.download_media(
            story.media,
            file=str(out_dir / target_file_prefix),
        )

        # Write metadata JSON
        meta_data = {
            "story_id": story_id,
            "peer": str(peer),
            "caption": caption,
            "uploaded_date": uploaded_date_iso,
            "media_type": media_type,
            "saved_file": str(downloaded_file) if downloaded_file else None,
        }
        meta_path = out_dir / f"{target_file_prefix}_metadata.json"
        meta_path.write_text(json.dumps(meta_data, indent=2, ensure_ascii=False), encoding="utf-8")

        return StoryDownloadResult(
            story_id=story_id,
            peer=peer,
            media_path=str(downloaded_file) if downloaded_file else None,
            metadata_path=str(meta_path),
            caption=caption,
            uploaded_date=uploaded_date_iso,
            media_type=media_type,
            success=True,
        )

    except Exception as e:
        logger.error(f"Failed to download story {story_id} for peer {peer}: {e}")
        return StoryDownloadResult(
            story_id=story_id,
            peer=peer,
            media_path=None,
            metadata_path=None,
            caption="",
            uploaded_date="",
            media_type="unknown",
            success=False,
            error=str(e),
        )


async def download_user_stories(
    client: TelegramClient,
    peer: Union[str, int],
    filter_mode: StoryFilterMode,
    base_dir: Path,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> List[StoryDownloadResult]:
    """Fetch and download public stories for a peer according to filter_mode."""
    all_stories = await fetch_peer_stories(client, peer)
    target_stories = filter_stories_by_mode(all_stories, filter_mode)

    results: List[StoryDownloadResult] = []
    total = len(target_stories)

    for idx, story in enumerate(target_stories, start=1):
        res = await download_single_story(client, peer, story.id, base_dir)
        results.append(res)
        if progress_callback:
            progress_callback(idx, total)

    return results
