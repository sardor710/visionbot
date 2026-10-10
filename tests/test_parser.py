import pytest
from datetime import datetime, timezone, timedelta
from telebot_downloader.core.parser import (
    TargetType,
    ParsedTarget,
    parse_telegram_input,
    StoryFilterMode,
)


def test_parse_public_channel_post_link():
    url = "https://t.me/telegram/1234"
    result = parse_telegram_input(url)
    assert result.target_type == TargetType.POST
    assert result.peer == "telegram"
    assert result.item_id == 1234


def test_parse_private_channel_post_link():
    url = "https://t.me/c/1234567890/567"
    result = parse_telegram_input(url)
    assert result.target_type == TargetType.POST
    assert result.peer == -1001234567890
    assert result.item_id == 567


def test_parse_public_story_link():
    url = "https://t.me/durov/s/12"
    result = parse_telegram_input(url)
    assert result.target_type == TargetType.STORY
    assert result.peer == "durov"
    assert result.item_id == 12


def test_parse_private_channel_story_link():
    url = "https://t.me/c/1234567890/s/89"
    result = parse_telegram_input(url)
    assert result.target_type == TargetType.STORY
    assert result.peer == -1001234567890
    assert result.item_id == 89


def test_parse_user_stories_command():
    text = "/user_stories durov 24h"
    result = parse_telegram_input(text)
    assert result.target_type == TargetType.USER_STORIES
    assert result.peer == "durov"
    assert result.story_filter == StoryFilterMode.LAST_24_HOURS

    text_all = "/user_stories @durov all"
    result_all = parse_telegram_input(text_all)
    assert result_all.target_type == TargetType.USER_STORIES
    assert result_all.peer == "durov"
    assert result_all.story_filter == StoryFilterMode.ALL


def test_parse_channel_posts_command():
    text = "/channel telegram"
    result = parse_telegram_input(text)
    assert result.target_type == TargetType.CHANNEL_POSTS
    assert result.peer == "telegram"

    text_id = "/channel -1001234567890"
    result_id = parse_telegram_input(text_id)
    assert result_id.target_type == TargetType.CHANNEL_POSTS
    assert result_id.peer == -1001234567890


def test_parse_invalid_input():
    with pytest.raises(ValueError):
        parse_telegram_input("https://google.com/search?q=test")
