"""Bot message and command dispatcher."""

from __future__ import annotations
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Callable, Any
from telethon import TelegramClient
from telebot_downloader.core.parser import (
    TargetType,
    ParsedTarget,
    parse_telegram_input,
    StoryFilterMode,
)
from telebot_downloader.downloader.engine import (
    download_single_post,
    download_channel_posts,
)
from telebot_downloader.downloader.stories import (
    download_single_story,
    download_user_stories,
)

logger = logging.getLogger(__name__)

HELP_MESSAGE = """
🤖 **Telegram Media & Story Downloader Bot**

Send me a Telegram link or use the commands below:

📌 **Download Post (Video/Photo + Caption & Date)**
• Send link directly: `https://t.me/channel/123`
• Or command: `/post https://t.me/channel/123`

📸 **Download Story from Link**
• Send story link directly: `https://t.me/username/s/1`
• Or command: `/story https://t.me/username/s/1`

👤 **Download User Public Stories**
• `/user_stories @username 24h` — Download stories from the last 24 hours
• `/user_stories @username all` — Download all current active public stories

📢 **Download Channel Media Posts**
• `/channel @channel_name` — Download all media posts from channel
• `/channel -1001234567890` — Download from channel ID

Downloads are saved with original captions and upload timestamps!
"""


class CommandAction(str, Enum):
    REPLY_TEXT = "reply_text"
    DOWNLOAD_POST = "download_post"
    DOWNLOAD_STORY = "download_story"
    DOWNLOAD_USER_STORIES = "download_user_stories"
    DOWNLOAD_CHANNEL_POSTS = "download_channel_posts"


@dataclass
class BotResponse:
    action: CommandAction
    message: str
    target: Optional[ParsedTarget] = None


def dispatch_user_command(text: str) -> BotResponse:
    """Analyze incoming text and dispatch to appropriate bot response action."""
    clean_text = text.strip()
    if clean_text in ("/start", "/help", "help"):
        return BotResponse(
            action=CommandAction.REPLY_TEXT,
            message=HELP_MESSAGE,
        )

    try:
        parsed = parse_telegram_input(clean_text)
        if parsed.target_type == TargetType.POST:
            return BotResponse(
                action=CommandAction.DOWNLOAD_POST,
                message=f"⏳ Downloading post {parsed.item_id} from `{parsed.peer}`...",
                target=parsed,
            )
        elif parsed.target_type == TargetType.STORY:
            return BotResponse(
                action=CommandAction.DOWNLOAD_STORY,
                message=f"⏳ Downloading story {parsed.item_id} from `{parsed.peer}`...",
                target=parsed,
            )
        elif parsed.target_type == TargetType.USER_STORIES:
            mode_desc = "last 24 hours" if parsed.story_filter == StoryFilterMode.LAST_24_HOURS else "all active"
            return BotResponse(
                action=CommandAction.DOWNLOAD_USER_STORIES,
                message=f"⏳ Fetching {mode_desc} stories for `{parsed.peer}`...",
                target=parsed,
            )
        elif parsed.target_type == TargetType.CHANNEL_POSTS:
            return BotResponse(
                action=CommandAction.DOWNLOAD_CHANNEL_POSTS,
                message=f"⏳ Starting channel media download for `{parsed.peer}`...",
                target=parsed,
            )
    except ValueError as e:
        return BotResponse(
            action=CommandAction.REPLY_TEXT,
            message=f"❌ Invalid command or link:\n{e}\n\nType /help for usage guidance.",
        )

    return BotResponse(
        action=CommandAction.REPLY_TEXT,
        message=HELP_MESSAGE,
    )


async def execute_bot_action(
    client: TelegramClient,
    response: BotResponse,
    base_dir: Path,
    reply_func: Callable[[str], Any],
) -> None:
    """Execute the download action and report results back via reply_func."""
    target = response.target
    if not target:
        await reply_func(response.message)
        return

    if response.action == CommandAction.DOWNLOAD_POST:
        await reply_func(response.message)
        res = await download_single_post(client, target.peer, target.item_id, base_dir)
        if res.success:
            cap_preview = f"\n📝 Caption: {res.caption[:200]}..." if res.caption else "\n📝 Caption: (None)"
            msg = (
                f"✅ **Post Downloaded Successfully!**\n"
                f"• Peer: `{res.peer}`\n"
                f"• Message ID: `{res.message_id}`\n"
                f"• Media Type: `{res.media_type}`\n"
                f"• Uploaded Date: `{res.uploaded_date}`{cap_preview}\n"
                f"• Saved File: `{res.media_path}`\n"
                f"• Metadata: `{res.metadata_path}`"
            )
        else:
            msg = f"❌ Failed to download post: {res.error}"
        await reply_func(msg)

    elif response.action == CommandAction.DOWNLOAD_STORY:
        await reply_func(response.message)
        res = await download_single_story(client, target.peer, target.item_id, base_dir)
        if res.success:
            cap_preview = f"\n📝 Caption: {res.caption[:200]}..." if res.caption else ""
            msg = (
                f"✅ **Story Downloaded Successfully!**\n"
                f"• Peer: `{res.peer}`\n"
                f"• Story ID: `{res.story_id}`\n"
                f"• Media Type: `{res.media_type}`\n"
                f"• Uploaded Date: `{res.uploaded_date}`{cap_preview}\n"
                f"• Saved File: `{res.media_path}`"
            )
        else:
            msg = f"❌ Failed to download story: {res.error}"
        await reply_func(msg)

    elif response.action == CommandAction.DOWNLOAD_USER_STORIES:
        await reply_func(response.message)
        results = await download_user_stories(
            client=client,
            peer=target.peer,
            filter_mode=target.story_filter,
            base_dir=base_dir,
        )
        successful = [r for r in results if r.success]
        msg = (
            f"✅ **Finished Stories Download for `{target.peer}`**\n"
            f"• Filter Mode: `{target.story_filter.value}`\n"
            f"• Total Processed: `{len(results)}`\n"
            f"• Successfully Downloaded: `{len(successful)}`\n"
            f"• Saved under: `{base_dir / 'stories' / str(target.peer)}`"
        )
        await reply_func(msg)

    elif response.action == CommandAction.DOWNLOAD_CHANNEL_POSTS:
        await reply_func(response.message)
        results = await download_channel_posts(
            client=client,
            peer=target.peer,
            base_dir=base_dir,
        )
        successful = [r for r in results if r.success]
        msg = (
            f"✅ **Finished Channel Posts Download for `{target.peer}`**\n"
            f"• Media Posts Downloaded: `{len(successful)}`\n"
            f"• Saved under: `{base_dir / 'posts' / str(target.peer)}`"
        )
        await reply_func(msg)
