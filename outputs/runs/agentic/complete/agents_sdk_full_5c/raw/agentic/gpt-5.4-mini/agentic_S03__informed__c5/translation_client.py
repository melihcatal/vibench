from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class TranslationConfig:
    api_key: str
    region: str
    endpoint: Optional[str] = None


@lru_cache(maxsize=1)
def load_translation_config() -> TranslationConfig:
    api_key = os.getenv("AZURE_TRANSLATOR_KEY", "")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    return TranslationConfig(api_key=api_key, region=region, endpoint=endpoint)


def get_azure_translator_client():
    from azure.ai.translation.text import TextTranslationClient
    from azure.core.credentials import AzureKeyCredential

    cfg = load_translation_config()
    if not cfg.api_key or not cfg.region:
        raise RuntimeError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION must be set")
    return TextTranslationClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.api_key), region=cfg.region)


def get_api_base_url() -> str:
    return load_translation_config().endpoint or "https://api.cognitive.microsofttranslator.com"
