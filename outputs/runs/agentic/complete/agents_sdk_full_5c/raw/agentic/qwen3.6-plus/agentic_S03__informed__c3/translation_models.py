"""Local request, response, and normalization helpers for General Text Translation.

Defines data models used across the translation integration files.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class TranslationRequest:
    text: str
    source_lang: str = ""
    target_lang: str = "EN"
    formality: str = "default"


@dataclass
class TranslationResponse:
    translated_text: str
    source_lang: str = ""
    target_lang: str = ""
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BatchTranslationRequest:
    texts: list[str]
    source_lang: str = ""
    target_lang: str = "EN"
    formality: str = "default"


@dataclass
class BatchTranslationResponse:
    results: list[TranslationResponse] = field(default_factory=list)

    @property
    def translated_texts(self) -> list[str]:
        return [r.translated_text for r in self.results]

    def to_dict(self) -> dict[str, Any]:
        return {"results": [r.to_dict() for r in self.results]}


def normalize_language_code(code: str) -> str:
    """Normalize language codes to DeepL format (e.g. 'en' -> 'EN')."""
    return code.strip().upper()[:2]


def normalize_formality(formality: str) -> str:
    allowed = {"default", "more", "less", "prefer_more", "prefer_less"}
    if formality in allowed:
        return formality
    return "default"


def build_request(
    text: str,
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
) -> TranslationRequest:
    return TranslationRequest(
        text=text,
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang),
        formality=normalize_formality(formality),
    )


def build_batch_request(
    texts: list[str],
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
) -> BatchTranslationRequest:
    return BatchTranslationRequest(
        texts=texts,
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang),
        formality=normalize_formality(formality),
    )


def deepl_result_to_response(result, target_lang: str) -> TranslationResponse:
    """Convert a deepl.TextResult to a TranslationResponse."""
    return TranslationResponse(
        translated_text=result.text,
        source_lang=result.detected_source_language or "",
        target_lang=target_lang.upper(),
    )
