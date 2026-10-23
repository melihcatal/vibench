import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class TextContentSafetyConfig:
    endpoint: str
    key: str


def _get_env(name: str) -> Optional[str]:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def load_text_content_safety_config() -> TextContentSafetyConfig:
    endpoint = _get_env("AZURE_CONTENT_SAFETY_ENDPOINT") or _get_env("AZURE_AI_CONTENT_SAFETY_ENDPOINT")
    key = _get_env("AZURE_CONTENT_SAFETY_KEY") or _get_env("AZURE_AI_CONTENT_SAFETY_KEY")
    if not endpoint:
        raise ValueError("Missing Text Content Safety endpoint. Set AZURE_CONTENT_SAFETY_ENDPOINT.")
    if not key:
        raise ValueError("Missing Text Content Safety key. Set AZURE_CONTENT_SAFETY_KEY.")
    return TextContentSafetyConfig(endpoint=endpoint, key=key)


@lru_cache(maxsize=1)
def get_text_content_safety_client() -> ContentSafetyClient:
    config = load_text_content_safety_config()
    return ContentSafetyClient(config.endpoint, AzureKeyCredential(config.key))


def build_text_content_safety_client(endpoint: str, key: str) -> ContentSafetyClient:
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))
