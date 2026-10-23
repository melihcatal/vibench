import os
from dataclasses import dataclass
from typing import Optional

from openai import AzureOpenAI


@dataclass(frozen=True)
class PlatformClientConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-05-01-preview"
    deployment: str = "gpt-4o-mini"


def load_platform_config() -> PlatformClientConfig:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
    return PlatformClientConfig(endpoint=endpoint, api_key=api_key, deployment=deployment, api_version=api_version)


def build_azure_openai_client(config: Optional[PlatformClientConfig] = None) -> AzureOpenAI:
    config = config or load_platform_config()
    return AzureOpenAI(
        api_key=config.api_key,
        api_version=config.api_version,
        azure_endpoint=config.endpoint,
    )
