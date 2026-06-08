from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, ClassVar

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class NetworkMode(str, Enum):
    MAINNET = "MAINNET"
    TESTNET = "TESTNET"


class Config(BaseSettings):
    NETWORK_MODE: NetworkMode = NetworkMode.TESTNET

    BOT_TOKEN: SecretStr

    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    BASE_URL: str

    DATABASE_SYSTEM: str = "postgresql"
    DATABASE_DRIVER: str = "asyncpg"
    DATABASE_NAME: SecretStr
    DATABASE_USER: SecretStr
    DATABASE_PASSWORD: SecretStr
    DATABASE_HOST: SecretStr
    DATABASE_PORT: SecretStr

    TON_MASTER_MNEMONICS: SecretStr
    MASTER_MNEMONICS: SecretStr
    BNB_RPC_URL: SecretStr
    ETH_RPC_URL: SecretStr
    ALCHEMY_NOTIFY_TOKEN: SecretStr
    ETH_ALCHEMY_WEBHOOK_ID: str
    ETH_ALCHEMY_WEBHOOK_SECRET: SecretStr
    BNB_ALCHEMY_WEBHOOK_ID: str
    BNB_ALCHEMY_WEBHOOK_SECRET: SecretStr
    TONCONSOLE_API_KEY: SecretStr
    TONCONSOLE_WEBHOOK_PATH: str = "/webhook/ton"

    REDIS_URL: SecretStr

    @property
    def API_URL(self) -> str:
        return f"{self.BASE_URL}/api"

    @property
    def is_mainnet(self) -> bool:
        return self.NETWORK_MODE == NetworkMode.MAINNET

    BACKEND_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent
    PROJECT_DIR: ClassVar[Path] = BACKEND_DIR.parent
    SETTINGS_FILE: ClassVar[Path] = (
        BACKEND_DIR / "settings.json"
        if (BACKEND_DIR / "settings.json").exists()
        else PROJECT_DIR / "settings.json"
    )
    ENV_FILE: ClassVar[Path] = (
        BACKEND_DIR / ".env"
        if (BACKEND_DIR / ".env").exists()
        else PROJECT_DIR / ".env"
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def __init__(self, **values: Any):
        super().__init__(**values)


config = Config()
