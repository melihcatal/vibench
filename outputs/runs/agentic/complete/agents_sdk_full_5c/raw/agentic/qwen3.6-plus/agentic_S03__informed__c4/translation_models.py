"""
Local request, response, and normalization helpers for General Text Translation.

Provides dataclasses and utilities for translation requests/responses
that work with the DeepL Translation API.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TranslationRequest:
    """Normalized translation request payload."""

    text: str
    source_lang: Optional[str] = None
    target_lang: str = "EN"
    formality: Optional[str] = None
    preserve_formatting: bool = True
    tag_handling: Optional[str] = None
    outline_detection: bool = True
    split_sentences: str = "1"
    non_splitting_tags: list[str] = field(default_factory=list)
    ignore_tags: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        """
        Validate the request and return a list of error messages.
        Returns empty list if valid.
        """
        errors: list[str] = []
        if not self.text or not self.text.strip():
            errors.append("Text cannot be empty")
        if not self.target_lang:
            errors.append("Target language is required")
        if self.formality and self.formality not in ("more", "less", "prefer_more", "prefer_less", "default"):
            errors.append(f"Invalid formality: {self.formality}")
        return errors


@dataclass
class TranslationResult:
    """Single translation result."""

    text: str
    detected_source_lang: Optional[str] = None
    model_info: Optional[str] = None


@dataclass
class TranslationResponse:
    """Normalized translation response from the provider."""

    translations: list[TranslationResult] = field(default_factory=list)
    character_count: int = 0
    character_limit: Optional[int] = None

    @property
    def is_success(self) -> bool:
        return len(self.translations) > 0

    @property
    def first_text(self) -> str:
        if self.translations:
            return self.translations[0].text
        return ""


def parse_deepl_response(raw_results: list[Any]) -> TranslationResponse:
    """
    Parse DeepL SDK response into our normalized TranslationResponse.

    Args:
        raw_results: List of deepl.TextResult objects from DeepL translate_text.

    Returns:
        Normalized TranslationResponse.
    """
    translations: list[TranslationResult] = []
    char_count = 0

    for result in raw_results:
        translations.append(TranslationResult(
            text=result.text,
            detected_source_lang=getattr(result, "detected_source_lang", None),
            model_info=None,  # DeepL does not expose model info
        ))
        char_count += len(result.text)

    return TranslationResponse(
        translations=translations,
        character_count=char_count,
    )


def normalize_source_language(lang_code: Optional[str]) -> Optional[str]:
    """
    Normalize source language code for DeepL.

    DeepL accepts None for auto-detect, or uppercase codes.
    Some languages require region variants (e.g., EN-US vs EN-GB).

    Args:
        lang_code: Raw language code or None for auto-detect.

    Returns:
        Normalized code or None.
    """
    if lang_code is None:
        return None
    code = lang_code.strip().upper()
    if code == "AUTO":
        return None
    return code


def extract_language_from_locale(locale: str) -> str:
    """
    Extract base language code from a locale string.

    Args:
        locale: e.g., 'en-US', 'pt-BR', 'fr'

    Returns:
        Base language code in uppercase, e.g., 'EN', 'PT', 'FR'
    """
    return locale.strip().split("-")[0].upper()


def build_tag_handling_config(html_mode: bool = False) -> dict:
    """
    Build tag handling configuration for DeepL.

    Args:
        html_mode: Whether to use HTML tag handling.

    Returns:
        Dict of kwargs for the DeepL translate_text call.
    """
    if html_mode:
        return {
            "tag_handling": "xml",
            "ignore_tags": ["script", "style", "code", "pre"],
            "outline_detection": False,
            "split_sentences": "0",
        }
    return {}


def merge_dictionary_translation_results(
    original: dict[str, str],
    translated_values: list[str],
    keys: list[str],
) -> dict[str, str]:
    """
    Merge translated values back into a dictionary, preserving original keys.

    Args:
        original: Original dictionary.
        translated_values: List of translated strings in key order.
        keys: Ordered list of keys matching translated_values.

    Returns:
        New dictionary with translated values and original keys.
    """
    result: dict[str, str] = {}
    for key, value in zip(keys, translated_values):
        result[key] = value
    return result
