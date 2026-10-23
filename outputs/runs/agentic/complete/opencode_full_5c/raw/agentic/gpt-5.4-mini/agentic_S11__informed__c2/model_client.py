import os
from dataclasses import dataclass

from openai import AzureOpenAI


@dataclass(frozen=True)
class PlatformConfig:
    endpoint: str
    api_key: str
    api_version: str
    deployment: str
    model: str


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        model=os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o-mini"),
    )


def build_platform_client() -> AzureOpenAI:
    cfg = load_platform_config()
    return AzureOpenAI(
        api_key=cfg.api_key, api_version=cfg.api_version, azure_endpoint=cfg.endpoint
    )
