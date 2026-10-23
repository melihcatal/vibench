import os
from dataclasses import dataclass
from typing import Optional

import deepl


@dataclass(frozen=True)
class TranslationConfig:
    auth_key: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


def load_config() -> TranslationConfig:
    return TranslationConfig(
        auth_key=os.getenv("DEEPL_AUTH_KEY", ""),
        source_lang=os.getenv("TRANSLATION_SOURCE_LANG"),
        target_lang=os.getenv("TRANSLATION_TARGET_LANG"),
    )


def create_client() -> deepl.Translator:
    config = load_config()
    if not config.auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return deepl.Translator(config.auth_key)
