from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    mime_type: str = "text/plain"


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: Optional[str] = None
    target_language: str = "en"
    mime_type: str = "text/plain"


@dataclass(slots=True)
class TranslationResult:
    text: str
    detected_source_language: Optional[str] = None
    provider: str = "google-cloud-translate"
    model: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BatchTranslationResult:
    translations: List[TranslationResult]
    provider: str = "google-cloud-translate"
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_texts(values: Sequence[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_dictionary_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in values.items()}


def build_translation_result(
    response: Mapping[str, Any], provider: str = "google-cloud-translate"
) -> TranslationResult:
    return TranslationResult(
        text=normalize_text(response.get("translatedText") or response.get("text")),
        detected_source_language=response.get("detectedLanguageCode")
        or response.get("detected_source_language"),
        provider=provider,
        model=response.get("model"),
        metadata=dict(response),
    )
