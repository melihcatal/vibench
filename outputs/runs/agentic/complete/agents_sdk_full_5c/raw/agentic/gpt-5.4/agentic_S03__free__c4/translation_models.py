from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    content_type: str = "text/plain"

    def as_azure_input(self) -> Dict[str, str]:
        return {"text": self.text}


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: List[str]
    source_language: Optional[str] = None
    target_language: str = "en"
    content_type: str = "text/plain"

    def as_azure_inputs(self) -> List[Dict[str, str]]:
        return [{"text": text} for text in self.texts]


@dataclass(slots=True)
class TranslationResult:
    text: str
    detected_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QualitySummary:
    summary: str
    issues: List[str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SafetyCheckResult:
    safe: bool
    categories: List[str]
    redacted_text: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    model: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_translations(items: Iterable[Mapping[str, Any]]) -> List[TranslationResult]:
    results: List[TranslationResult] = []
    for item in items:
        translations = item.get("translations") or []
        first = translations[0] if translations else {}
        detected = item.get("detectedLanguage") or {}
        results.append(
            TranslationResult(
                text=first.get("text", ""),
                detected_language=detected.get("language"),
                target_language=first.get("to"),
                raw=dict(item),
            )
        )
    return results


def normalize_dictionary_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): str(value) for key, value in data.items()}
