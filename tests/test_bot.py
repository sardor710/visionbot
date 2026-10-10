import pytest
from telebot_downloader.bot.handlers import (
    dispatch_user_command,
    BotResponse,
    CommandAction,
)
from telebot_downloader.core.parser import StoryFilterMode


def test_bot_dispatch_start():
    resp = dispatch_user_command("/start")
    assert resp.action == CommandAction.REPLY_TEXT
    assert "Telegram Media & Story Downloader" in resp.message


def test_bot_dispatch_help():
    resp = dispatch_user_command("/help")
    assert resp.action == CommandAction.REPLY_TEXT
    assert "/user_stories" in resp.message
    assert "/channel" in resp.message


def test_bot_dispatch_post_link():
    resp = dispatch_user_command("https://t.me/telegram/100")
    assert resp.action == CommandAction.DOWNLOAD_POST
    assert resp.target.peer == "telegram"
    assert resp.target.item_id == 100


def test_bot_dispatch_story_link():
    resp = dispatch_user_command("https://t.me/durov/s/5")
    assert resp.action == CommandAction.DOWNLOAD_STORY
    assert resp.target.peer == "durov"
    assert resp.target.item_id == 5


def test_bot_dispatch_user_stories():
    resp = dispatch_user_command("/user_stories durov 24h")
    assert resp.action == CommandAction.DOWNLOAD_USER_STORIES
    assert resp.target.peer == "durov"
    assert resp.target.story_filter == StoryFilterMode.LAST_24_HOURS


def test_bot_dispatch_channel():
    resp = dispatch_user_command("/channel @tech_news")
    assert resp.action == CommandAction.DOWNLOAD_CHANNEL_POSTS
    assert resp.target.peer == "tech_news"
