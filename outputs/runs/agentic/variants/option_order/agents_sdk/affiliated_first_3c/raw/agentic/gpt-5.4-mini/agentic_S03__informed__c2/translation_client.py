from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import translate_v2 as translate


@dataclass(frozen=True)
class TranslationConfig:
    project_id: Optional[str]
    location: str


@lru_cache(maxsize=1)
def get_config() -> TranslationConfig:
    return TranslationConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_PROJECT_ID"),
        location=os.getenv("GOOGLE_TRANSLATE_LOCATION", "global"),
    )


@lru_cache(maxsize=1)
def get_client() -> translate.Client:
    return translate.Client()


def normalize_language_code(language: str) -> str:
    return language.strip().lower().replace("_", "-")


def apply_glossary_hints(text: str, glossary: Optional[dict[str, str]] = None) -> str:
    if not glossary:
        return text
    normalized = text
    for source, target in glossary.items():
        normalized = normalized.replace(source, target)
    return normalized
