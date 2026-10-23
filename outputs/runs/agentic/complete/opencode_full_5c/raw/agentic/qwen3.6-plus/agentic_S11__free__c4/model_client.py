from __future__ import annotations

import os
from typing import Any, Optional

from openai import OpenAI, AsyncOpenAI


DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096


class PlatformClientConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        project: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.organization = organization or os.environ.get("OPENAI_ORGANIZATION", None)
        self.project = project or os.environ.get("OPENAI_PROJECT", None)
        self.base_url = base_url or os.environ.get(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        self.timeout = timeout
        self.max_retries = max_retries

    def build_client(self) -> OpenAI:
        kwargs: dict[str, Any] = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }
        if self.organization:
            kwargs["organization"] = self.organization
        if self.project:
            kwargs["project"] = self.project
        return OpenAI(**kwargs)

    def build_async_client(self) -> AsyncOpenAI:
        kwargs: dict[str, Any] = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }
        if self.organization:
            kwargs["organization"] = self.organization
        if self.project:
            kwargs["project"] = self.project
        return AsyncOpenAI(**kwargs)


def get_default_config() -> PlatformClientConfig:
    return PlatformClientConfig()


def create_openai_client(
    config: Optional[PlatformClientConfig] = None,
) -> OpenAI:
    cfg = config or get_default_config()
    return cfg.build_client()


def create_openai_async_client(
    config: Optional[PlatformClientConfig] = None,
) -> AsyncOpenAI:
    cfg = config or get_default_config()
    return cfg.build_async_client()
