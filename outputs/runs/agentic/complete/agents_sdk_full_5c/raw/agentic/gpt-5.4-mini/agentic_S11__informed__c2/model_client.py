from __future__ import annotations

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


@lru_cache(maxsize=1)
def load_config() -> PlatformConfig:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    return PlatformConfig(endpoint=endpoint, api_key=api_key, api_version=api_version, deployment=deployment)


@lru_cache(maxsize=1)
def get_client() -> AzureOpenAI:
    cfg = load_config()
    return AzureOpenAI(api_key=cfg.api_key, azure_endpoint=cfg.endpoint, api_version=cfg.api_version)


def get_deployment() -> str:
    return load_config().deployment


def has_credentials() -> bool:
    cfg = load_config()
    return bool(cfg.endpoint and cfg.api_key)
