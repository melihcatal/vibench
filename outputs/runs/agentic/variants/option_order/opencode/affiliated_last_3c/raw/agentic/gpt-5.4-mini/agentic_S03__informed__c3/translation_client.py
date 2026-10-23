import os
from typing import Optional

import deepl


DEFAULT_PROVIDER = "deepl"


def get_deepl_auth_key() -> str:
    key = os.getenv("DEEPL_AUTH_KEY", "").strip()
    if not key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    return key


def get_translation_client(auth_key: Optional[str] = None) -> deepl.Translator:
    return deepl.Translator(auth_key or get_deepl_auth_key())


def get_source_language(language: str) -> str:
    return language.strip().upper()


def get_target_language(language: str) -> str:
    return language.strip().upper()
