"""Parser for Telegram links, usernames, and download commands."""

from __future__ import annotations
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class TargetType(str, Enum):
    POST = "post"
    STORY = "story"
    USER_STORIES = "user_stories"
    CHANNEL_POSTS = "channel_posts"


class StoryFilterMode(str, Enum):
    ALL = "all"
    LAST_24_HOURS = "24h"


@dataclass
class ParsedTarget:
    target_type: TargetType
    peer: Union[str, int]
    item_id: Optional[int] = None
    story_filter: StoryFilterMode = StoryFilterMode.ALL
    raw_input: str = ""


# Regex patterns for Telegram URLs
RE_PRIVATE_STORY = re.compile(
    r"(?:https?://)?(?:t\.me|telegram\.me)/c/(\d+)/s/(\d+)/?", re.IGNORECASE
)
RE_PUBLIC_STORY = re.compile(
    r"(?:https?://)?(?:t\.me|telegram\.me)/([a-zA-Z0-9_]+)/s/(\d+)/?", re.IGNORECASE
)
RE_PRIVATE_POST = re.compile(
    r"(?:https?://)?(?:t\.me|telegram\.me)/c/(\d+)/(\d+)/?", re.IGNORECASE
)
RE_PUBLIC_POST = re.compile(
    r"(?:https?://)?(?:t\.me|telegram\.me)/([a-zA-Z0-9_]+)/(\d+)/?", re.IGNORECASE
)


def normalize_peer(peer_str: str) -> Union[str, int]:
    """Normalize username or ID to appropriate peer representation."""
    cleaned = peer_str.strip().lstrip("@")
    if cleaned.startswith("-100") and cleaned[4:].isdigit():
        return int(cleaned)
    if cleaned.startswith("-") and cleaned[1:].isdigit():
        return int(cleaned)
    if cleaned.isdigit():
        return int(cleaned)
    return cleaned


def parse_telegram_input(input_text: str) -> ParsedTarget:
    """Parse telegram links or bot commands into structured ParsedTarget.

    Raises ValueError if input cannot be parsed.
    """
    text = input_text.strip()
    if not text:
        raise ValueError("Input text cannot be empty.")

    # 1. Private story link: https://t.me/c/1234567890/s/89
    m_priv_story = RE_PRIVATE_STORY.match(text)
    if m_priv_story:
        channel_id_num = int(m_priv_story.group(1))
        # MTProto private channel peer ID starts with -100
        peer_id = -1000000000000 - channel_id_num if channel_id_num < 1000000000000 else -channel_id_num
        return ParsedTarget(
            target_type=TargetType.STORY,
            peer=peer_id,
            item_id=int(m_priv_story.group(2)),
            raw_input=text,
        )

    # 2. Public story link: https://t.me/durov/s/12
    m_pub_story = RE_PUBLIC_STORY.match(text)
    if m_pub_story:
        return ParsedTarget(
            target_type=TargetType.STORY,
            peer=m_pub_story.group(1),
            item_id=int(m_pub_story.group(2)),
            raw_input=text,
        )

    # 3. Private post link: https://t.me/c/1234567890/567
    m_priv_post = RE_PRIVATE_POST.match(text)
    if m_priv_post:
        channel_id_num = int(m_priv_post.group(1))
        peer_id = -1000000000000 - channel_id_num if channel_id_num < 1000000000000 else -channel_id_num
        return ParsedTarget(
            target_type=TargetType.POST,
            peer=peer_id,
            item_id=int(m_priv_post.group(2)),
            raw_input=text,
        )

    # 4. Public post link: https://t.me/telegram/1234
    m_pub_post = RE_PUBLIC_POST.match(text)
    if m_pub_post:
        return ParsedTarget(
            target_type=TargetType.POST,
            peer=m_pub_post.group(1),
            item_id=int(m_pub_post.group(2)),
            raw_input=text,
        )

    # 5. Commands: /user_stories <username|id> [24h|all]
    if text.startswith("/user_stories"):
        parts = text.split()
        if len(parts) < 2:
            raise ValueError("Usage: /user_stories <username|id> [24h|all]")
        peer = normalize_peer(parts[1])
        filter_mode = StoryFilterMode.ALL
        if len(parts) >= 3 and parts[2].lower() in ("24h", "24", "today"):
            filter_mode = StoryFilterMode.LAST_24_HOURS
        return ParsedTarget(
            target_type=TargetType.USER_STORIES,
            peer=peer,
            story_filter=filter_mode,
            raw_input=text,
        )

    # 6. Commands: /channel <name|id>
    if text.startswith("/channel"):
        parts = text.split()
        if len(parts) < 2:
            raise ValueError("Usage: /channel <channel_username|channel_id>")
        peer = normalize_peer(parts[1])
        return ParsedTarget(
            target_type=TargetType.CHANNEL_POSTS,
            peer=peer,
            raw_input=text,
        )

    # 7. Commands: /post <link>
    if text.startswith("/post"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            raise ValueError("Usage: /post <telegram_post_link>")
        return parse_telegram_input(parts[1])

    # 8. Commands: /story <link>
    if text.startswith("/story"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            raise ValueError("Usage: /story <telegram_story_link>")
        return parse_telegram_input(parts[1])

    raise ValueError(f"Unrecognized Telegram input or command: {text}")
