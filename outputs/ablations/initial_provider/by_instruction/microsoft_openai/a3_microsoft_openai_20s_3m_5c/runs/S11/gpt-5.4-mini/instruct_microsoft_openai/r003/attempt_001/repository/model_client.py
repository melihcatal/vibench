import os
from dataclasses import dataclass

from openai import AzureOpenAI


@dataclass(frozen=True)
class PlatformConfig:
    azure_endpoint: str
    api_key: str
    api_version: str
    deployment: str


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
    )


def build_platform_client(config: PlatformConfig | None = None) -> AzureOpenAI:
    cfg = config or load_platform_config()
    return AzureOpenAI(
        azure_endpoint=cfg.azure_endpoint,
        api_key=cfg.api_key,
        api_version=cfg.api_version,
    )
