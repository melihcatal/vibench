import os
from dataclasses import dataclass

from openai import AzureOpenAI


@dataclass
class PlatformConfig:
    endpoint: str
    api_key: str
    api_version: str
    model: str


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        model=os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o-mini"),
    )


def get_platform_client() -> AzureOpenAI:
    cfg = load_platform_config()
    return AzureOpenAI(
        api_key=cfg.api_key, azure_endpoint=cfg.endpoint, api_version=cfg.api_version
    )
