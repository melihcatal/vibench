from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str]
    target_language: str
    content_type: str = "text/plain"
    glossary_config: Optional[Dict[str, Any]] = None

    def as_google_translate_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "contents": [self.text],
            "target_language_code": self.target_language,
            "mime_type": self.content_type,
        }
        if self.source_language:
            payload["source_language_code"] = self.source_language
        if self.glossary_config:
            payload["glossary_config"] = self.glossary_config
        return payload


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: List[str]
    source_language: Optional[str]
    target_language: str
    content_type: str = "text/plain"

    def as_google_translate_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "contents": self.texts,
            "target_language_code": self.target_language,
            "mime_type": self.content_type,
        }
        if self.source_language:
            payload["source_language_code"] = self.source_language
        return payload


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_language: Optional[str] = None
    provider: str = "google-cloud-translate"
    model: str = "translation-llm"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BatchTranslationResult:
    translations: List[TranslationResult]
    provider: str = "google-cloud-translate"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QualitySummaryResult:
    summary: str
    issues: List[str]
    provider: str = "openai"
    model: str = "gpt-4o-mini"


@dataclass(slots=True)
class SafetyCheckResult:
    unsafe: bool
    categories: List[str]
    rationale: str
    provider: str = "openai"
    model: str = "omni-moderation-latest"


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    dimensions: int
    provider: str = "openai"
    model: str = "text-embedding-3-small"


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str
    provider: str = "elevenlabs"
    model: str = "eleven_multilingual_v2"


def normalize_translation_item(item: Mapping[str, Any]) -> TranslationResult:
    return TranslationResult(
        translated_text=str(item.get("translated_text", "")),
        detected_language=item.get("detected_language_code"),
        metadata=dict(item),
    )


def normalize_translation_items(items: Iterable[Mapping[str, Any]]) -> List[TranslationResult]:
    return [normalize_translation_item(item) for item in items]
