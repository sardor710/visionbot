"""Main CLI and entrypoint for Telegram Downloader Bot."""

from __future__ import annotations
import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Ensure src root is in sys.path when running main.py directly
src_dir = Path(__file__).resolve().parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from telethon import events, TelegramClient
from telebot_downloader.core.client import (
    load_config_from_env,
    create_telethon_client,
    initialize_client,
)
from telebot_downloader.bot.handlers import (
    dispatch_user_command,
    execute_bot_action,
    CommandAction,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("telebot_downloader")


async def run_bot_service(env_path: Path | None = None) -> None:
    """Start and run the Telegram client with event listeners."""
    config = load_config_from_env(env_path)
    client = create_telethon_client(config)

    logger.info("Initializing client session...")
    await initialize_client(client, phone=config.phone, bot_token=config.bot_token)
    me = await client.get_me()
    logger.info(f"Signed in successfully as: {me.first_name} (@{me.username or me.id})")

    # Ensure downloads directory exists
    config.download_dir.mkdir(parents=True, exist_ok=True)

    @client.on(events.NewMessage(incoming=True))
    async def on_new_message(event: events.NewMessage.Event) -> None:
        text = event.raw_text
        if not text:
            return

        logger.info(f"Received message from peer {event.chat_id}: {text[:80]}")
        response = dispatch_user_command(text)

        async def reply_func(msg_text: str) -> None:
            await event.reply(msg_text)

        await execute_bot_action(
            client=client,
            response=response,
            base_dir=config.download_dir,
            reply_func=reply_func,
        )

    logger.info("Bot is active and listening for links and commands. Press Ctrl+C to stop.")
    await client.run_until_disconnected()


async def run_auth_interactive(env_path: Path | None = None) -> None:
    """Interactively authenticate the Telegram user session and save session file."""
    config = load_config_from_env(env_path)
    client = create_telethon_client(config)
    await client.connect()

    if not await client.is_user_authorized():
        logger.info("User is not authorized. Initiating login process...")
        phone = config.phone or input("Enter your phone number (with country code, e.g. +123456789): ")
        await client.send_code_request(phone)
        code = input("Enter the Telegram verification code received: ")
        try:
            await client.sign_in(phone, code)
        except Exception as e:
            if "password" in str(e).lower():
                pw = input("2-Step Verification Password: ")
                await client.sign_in(password=pw)
            else:
                raise e
    me = await client.get_me()
    logger.info(f"Authentication complete! Signed in as: {me.first_name} (@{me.username or me.id})")
    logger.info(f"Session saved to '{config.session_name}.session'. You can now run the bot.")
    await client.disconnect()


async def run_direct_cli_download(target_str: str, env_path: Path | None = None) -> None:
    """Directly download a link or command target via CLI without running long-lived bot service."""
    config = load_config_from_env(env_path)
    client = create_telethon_client(config)
    await initialize_client(client, phone=config.phone, bot_token=config.bot_token)

    response = dispatch_user_command(target_str)
    print(f">> Action: {response.action.value}")
    print(f">> Status: {response.message}")

    async def console_reply(msg: str) -> None:
        print(f"\n[Bot]: {msg}")

    await execute_bot_action(
        client=client,
        response=response,
        base_dir=config.download_dir,
        reply_func=console_reply,
    )
    await client.disconnect()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Telegram Media & Story Downloader via Telethon",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the bot service listening for commands and links",
    )
    parser.add_argument(
        "--auth",
        action="store_true",
        help="Interactively authenticate Telegram user account session",
    )
    parser.add_argument(
        "--download",
        type=str,
        help="Download directly via link or command string (e.g. 'https://t.me/durov/s/1')",
    )
    parser.add_argument(
        "--env",
        type=Path,
        default=None,
        help="Path to custom .env configuration file",
    )

    args = parser.parse_args()

    if args.auth:
        asyncio.run(run_auth_interactive(args.env))
    elif args.download:
        asyncio.run(run_direct_cli_download(args.download, args.env))
    elif args.run:
        asyncio.run(run_bot_service(args.env))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
