"""Translate live captions into another language using DeepL API."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Sequence

import deepl

from speech_models import FinalTranscript, PartialTranscript


DEEPL_AUTH_ENV = "DEEPL_AUTH_KEY"

SUPPORTED_SOURCE_LANGS = [
    "EN", "DE", "FR", "ES", "IT", "NL", "PL", "PT", "RU",
    "JA", "ZH", "BG", "CS", "DA", "EL", "ET", "FI", "HU",
    "LV", "LT", "RO", "SK", "SL", "SV", "UK",
]


@dataclass
class TranslatedCaption:
    """Represents a translated caption segment."""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    is_final: bool
    raw_response: dict[str, Any] | None = None


def _get_deepl_client() -> deepl.Translator:
    """Create a DeepL Translator client using the API key from environment."""
    auth_key = os.environ.get(DEEPL_AUTH_ENV)
    if not auth_key:
        raise EnvironmentError(
            f"Environment variable {DEEPL_AUTH_ENV} is not set. "
            "Configure your DeepL auth key."
        )
    return deepl.Translator(auth_key)


def _normalize_language_code(lang: str) -> str:
    """Normalize a language code to DeepL's uppercase format."""
    return lang.strip().upper().replace("-", "_")


async def translate_captions(
    captions: AsyncIterator[PartialTranscript | FinalTranscript],
    target_language: str = "ES",
    source_language: str = "EN",
    formality: str | None = None,
    preserve_formatting: bool = True,
) -> AsyncIterator[TranslatedCaption]:
    """
    Translate live caption transcripts into another language using DeepL.

    Parameters
    ----------
    captions : AsyncIterator
        Async iterator of PartialTranscript or FinalTranscript objects.
    target_language : str
        Target language code (e.g. "ES", "FR", "DE").
    source_language : str
        Source language code (e.g. "EN").
    formality : str | None
        "more" or "less" formality, or None for default.
    preserve_formatting : bool
        Whether to preserve original formatting.
    """
    client = _get_deepl_client()
    target = _normalize_language_code(target_language)
    source = _normalize_language_code(source_language)

    translate_kwargs: dict[str, Any] = {
        "source_lang": source,
        "target_lang": target,
        "preserve_formatting": preserve_formatting,
    }
    if formality:
        translate_kwargs["formality"] = formality

    async for caption in captions:
        if isinstance(caption, FinalTranscript):
            is_final = True
        else:
            is_final = False

        if not caption.text or caption.text.isspace():
            yield TranslatedCaption(
                original_text=caption.text,
                translated_text="",
                source_language=source,
                target_language=target,
                is_final=is_final,
            )
            continue

        result = client.translate_text(
            caption.text,
            **translate_kwargs,
        )
        translated = result.text

        yield TranslatedCaption(
            original_text=caption.text,
            translated_text=translated,
            source_language=source,
            target_language=target,
            is_final=is_final,
        )


async def translate_batch(
    texts: Sequence[str],
    target_language: str = "ES",
    source_language: str = "EN",
    formality: str | None = None,
) -> list[str]:
    """Translate a batch of caption texts using DeepL."""
    client = _get_deepl_client()
    target = _normalize_language_code(target_language)
    source = _normalize_language_code(source_language)

    translate_kwargs: dict[str, Any] = {
        "source_lang": source,
        "target_lang": target,
    }
    if formality:
        translate_kwargs["formality"] = formality

    result = client.translate_text(texts, **translate_kwargs)
    return [t.text for t in result]
