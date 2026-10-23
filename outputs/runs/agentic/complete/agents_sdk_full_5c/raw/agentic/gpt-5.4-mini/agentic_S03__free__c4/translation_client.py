"""Helper utilities for DeepL translation client configuration."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import deepl

DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_USE_FREE_ENV = "DEEPL_USE_FREE_API"


@lru_cache(maxsize=1)
def get_deepl_client() -> deepl.Translator:
    auth_key = os.environ.get(DEEPL_AUTH_KEY_ENV, "")
    use_free_api = os.environ.get(DEEPL_USE_FREE_ENV, "false").lower() in {"1", "true", "yes"}
    return deepl.Translator(auth_key, server_url="https://api-free.deepl.com" if use_free_api else "https://api.deepl.com")


def get_source_language(source_lang: Optional[str]) -> Optional[str]:
    return source_lang.upper() if source_lang else None


def get_target_language(target_lang: Optional[str]) -> str:
    return (target_lang or os.environ.get("TRANSLATION_TARGET_LANG", "EN-US")).upper()


__all__ = ["get_deepl_client", "get_source_language", "get_target_language", "DEEPL_AUTH_KEY_ENV", "DEEPL_USE_FREE_ENV"]
