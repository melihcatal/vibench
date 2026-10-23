import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import AzureOpenAI


@dataclass(frozen=True)
class PlatformConfig:
    endpoint: str
    api_key: str
    api_version: str
    deployment: str
    model: str
    locale: str


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


@lru_cache(maxsize=1)
def load_config() -> PlatformConfig:
    return PlatformConfig(
        endpoint=_env("AZURE_OPENAI_ENDPOINT"),
        api_key=_env("AZURE_OPENAI_API_KEY"),
        api_version=_env("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        deployment=_env(
            "AZURE_OPENAI_DEPLOYMENT", _env("AZURE_OPENAI_MODEL", "gpt-4o-mini")
        ),
        model=_env("AZURE_OPENAI_MODEL", "gpt-4o-mini"),
        locale=_env("TARGET_LOCALE", "es"),
    )


@lru_cache(maxsize=1)
def get_client() -> AzureOpenAI:
    cfg = load_config()
    return AzureOpenAI(
        azure_endpoint=cfg.endpoint, api_key=cfg.api_key, api_version=cfg.api_version
    )


def deployment_name(name: Optional[str] = None) -> str:
    return name or load_config().deployment
