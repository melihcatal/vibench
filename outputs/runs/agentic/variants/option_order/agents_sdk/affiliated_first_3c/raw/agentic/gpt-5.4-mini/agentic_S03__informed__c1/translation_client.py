from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from deepl import AuthKeyManager, DeepLClient


@dataclass(frozen=True)
class TranslationConfig:
    auth_key: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


def load_translation_config() -> TranslationConfig:
    return TranslationConfig(
        auth_key=os.environ.get("DEEPL_AUTH_KEY", ""),
        source_lang=os.environ.get("TRANSLATION_SOURCE_LANG"),
        target_lang=os.environ.get("TRANSLATION_TARGET_LANG"),
    )


def build_translation_client(config: TranslationConfig | None = None) -> DeepLClient:
    cfg = config or load_translation_config()
    if not cfg.auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL API")
    return DeepLClient(auth_key=AuthKeyManager(cfg.auth_key))


def infer_target_lang(config: TranslationConfig | None = None) -> Optional[str]:
    cfg = config or load_translation_config()
    return cfg.target_lang


def infer_source_lang(config: TranslationConfig | None = None) -> Optional[str]:
    cfg = config or load_translation_config()
    return cfg.source_lang
