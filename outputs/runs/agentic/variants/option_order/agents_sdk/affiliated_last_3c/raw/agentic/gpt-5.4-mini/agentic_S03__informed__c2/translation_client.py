from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient


@dataclass(frozen=True)
class TranslationConfig:
    endpoint: str
    key: str
    region: str
    target_language: str = "en"


@lru_cache(maxsize=1)
def load_config() -> TranslationConfig:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
    region = os.environ.get("AZURE_TRANSLATOR_REGION", "global")
    return TranslationConfig(endpoint=endpoint, key=key, region=region)


@lru_cache(maxsize=1)
def get_client() -> TextTranslationClient:
    cfg = load_config()
    return TextTranslationClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.key), region=cfg.region)


def get_default_target_language() -> str:
    return os.environ.get("TARGET_LANGUAGE", load_config().target_language)
