from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import openai


@dataclass(frozen=True)
class LiveCaptionTranslationConfig:
    api_key: Optional[str]
    model: str
    target_language: str
    source_language: Optional[str]


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_live_caption_translation_config() -> LiveCaptionTranslationConfig:
    return LiveCaptionTranslationConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
        target_language=os.getenv("LIVE_CAPTION_TARGET_LANGUAGE", "en"),
        source_language=os.getenv("LIVE_CAPTION_SOURCE_LANGUAGE"),
    )


@lru_cache(maxsize=1)
def get_openai_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate_live_caption(text: str, target_language: Optional[str] = None, source_language: Optional[str] = None) -> str:
    config = load_live_caption_translation_config()
    destination = target_language or config.target_language
    source = source_language or config.source_language
    prompt = f"Translate the following live caption into {destination}."
    if source:
        prompt = f"Translate the following live caption from {source} into {destination}."
    response = get_openai_client().responses.create(
        model=config.model,
        input=[
            {"role": "system", "content": "You translate live meeting captions accurately and concisely."},
            {"role": "user", "content": f"{prompt}\n\n{text}"},
        ],
    )
    return response.output_text.strip()


__all__ = [
    "LiveCaptionTranslationConfig",
    "get_openai_client",
    "load_live_caption_translation_config",
    "translate_live_caption",
]
