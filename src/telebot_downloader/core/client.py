"""Telethon client session management and authentication."""

from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from telethon import TelegramClient


@dataclass
class ClientConfig:
    api_id: int
    api_hash: str
    phone: Optional[str] = None
    bot_token: Optional[str] = None
    session_name: str = "user_account_session"
    download_dir: Path = Path("downloads")


def load_config_from_env(env_path: Optional[str | Path] = None) -> ClientConfig:
    """Load client configuration from .env or environment variables."""
    if env_path:
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()

    api_id_raw = os.getenv("TELEGRAM_API_ID")
    if not api_id_raw:
        raise ValueError(
            "TELEGRAM_API_ID is required. Set it in .env or as environment variable."
        )

    api_hash = os.getenv("TELEGRAM_API_HASH")
    if not api_hash:
        raise ValueError(
            "TELEGRAM_API_HASH is required. Set it in .env or as environment variable."
        )

    phone = os.getenv("TELEGRAM_PHONE")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    session_name = os.getenv("TELEGRAM_SESSION_NAME", "user_account_session")
    download_dir = Path(os.getenv("DOWNLOAD_DIR", "downloads"))

    return ClientConfig(
        api_id=int(api_id_raw),
        api_hash=api_hash,
        phone=phone,
        bot_token=bot_token,
        session_name=session_name,
        download_dir=download_dir,
    )


def create_telethon_client(config: ClientConfig) -> TelegramClient:
    """Create a Telethon TelegramClient instance based on configuration."""
    session_path = Path(config.session_name)
    client = TelegramClient(
        str(session_path),
        config.api_id,
        config.api_hash,
    )
    return client


async def initialize_client(
    client: TelegramClient,
    phone: Optional[str] = None,
    bot_token: Optional[str] = None,
) -> TelegramClient:
    """Connect and authenticate the Telethon client."""
    if bot_token:
        await client.start(bot_token=bot_token)
    elif phone:
        await client.start(phone=phone)
    else:
        await client.start()
    return client
