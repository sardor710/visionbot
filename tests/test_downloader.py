import pytest
from datetime import datetime, timezone, timedelta
from telebot_downloader.downloader.stories import (
    filter_stories_by_mode,
    StoryFilterMode,
    MockStory,
)
from telebot_downloader.downloader.engine import (
    format_post_metadata,
    build_output_filepath,
)


def test_story_filtering_24h_vs_all():
    now = datetime.now(timezone.utc)
    story_recent = MockStory(story_id=1, date=now - timedelta(hours=3), caption="Recent story")
    story_old = MockStory(story_id=2, date=now - timedelta(hours=28), caption="Old story")
    all_stories = [story_recent, story_old]

    filtered_24h = filter_stories_by_mode(all_stories, StoryFilterMode.LAST_24_HOURS, current_time=now)
    assert len(filtered_24h) == 1
    assert filtered_24h[0].story_id == 1

    filtered_all = filter_stories_by_mode(all_stories, StoryFilterMode.ALL, current_time=now)
    assert len(filtered_all) == 2


def test_post_metadata_formatting():
    post_date = datetime(2026, 10, 10, 12, 0, 0, tzinfo=timezone.utc)
    meta = format_post_metadata(
        peer="my_channel",
        message_id=42,
        caption="Sample test caption",
        date=post_date,
        media_type="video",
    )
    assert meta["peer"] == "my_channel"
    assert meta["message_id"] == 42
    assert meta["caption"] == "Sample test caption"
    assert "2026-10-10" in meta["uploaded_date"]
    assert meta["media_type"] == "video"


def test_build_output_filepath(tmp_path):
    dest = build_output_filepath(
        base_dir=tmp_path,
        category="posts",
        peer="channel123",
        item_id=99,
        filename="clip.mp4",
    )
    assert "channel123" in str(dest)
    assert "99_clip.mp4" in str(dest)
