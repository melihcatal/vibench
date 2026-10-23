import os
from dataclasses import dataclass
from typing import Optional

from openai import AzureOpenAI


@dataclass(frozen=True)
class PlatformConfig:
    endpoint: str
    api_key: str
    api_version: str
    deployment: str


def load_platform_config() -> PlatformConfig:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    return PlatformConfig(endpoint=endpoint, api_key=api_key, api_version=api_version, deployment=deployment)


def create_platform_client(config: Optional[PlatformConfig] = None) -> AzureOpenAI:
    cfg = config or load_platform_config()
    return AzureOpenAI(azure_endpoint=cfg.endpoint, api_key=cfg.api_key, api_version=cfg.api_version)
