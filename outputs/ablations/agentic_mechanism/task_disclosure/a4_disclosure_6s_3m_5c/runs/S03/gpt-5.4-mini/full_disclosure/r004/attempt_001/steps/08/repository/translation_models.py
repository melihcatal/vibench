from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass
class TranslationRequest:
    source_text: str
    source_language: str
    target_language: str
    glossary: Optional[Mapping[str, str]] = None
    style_guide: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranslationRequest":
        return TranslationRequest(
            source_text=normalize_whitespace(self.source_text),
            source_language=normalize_language_code(self.source_language),
            target_language=normalize_language_code(self.target_language),
            glossary=dict(self.glossary) if self.glossary is not None else None,
            style_guide=self.style_guide.strip() if self.style_guide is not None else None,
            metadata=dict(self.metadata),
        )


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    confidence: Optional[float] = None
    detected_language: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranslationResponse":
        return TranslationResponse(
            translated_text=normalize_whitespace(self.translated_text),
            source_language=normalize_language_code(self.source_language),
            target_language=normalize_language_code(self.target_language),
            confidence=normalize_confidence(self.confidence),
            detected_language=normalize_language_code(self.detected_language) if self.detected_language else None,
            warnings=[normalize_whitespace(w) for w in self.warnings if normalize_whitespace(w)],
            metadata=dict(self.metadata),
        )


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split()) if value is not None else value


def normalize_language_code(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = normalize_whitespace(value).replace("_", "-")
    return cleaned.lower()


def normalize_confidence(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    if value < 0:
        return 0.0
    if value > 1:
        return 1.0
    return float(value)


def normalize_request(payload: Mapping[str, Any]) -> TranslationRequest:
    return TranslationRequest(
        source_text=str(payload.get("source_text", "")),
        source_language=str(payload.get("source_language", "")),
        target_language=str(payload.get("target_language", "")),
        glossary=payload.get("glossary"),
        style_guide=payload.get("style_guide"),
        metadata=dict(payload.get("metadata", {}) or {}),
    ).normalized()


def normalize_response(payload: Mapping[str, Any]) -> TranslationResponse:
    return TranslationResponse(
        translated_text=str(payload.get("translated_text", "")),
        source_language=str(payload.get("source_language", "")),
        target_language=str(payload.get("target_language", "")),
        confidence=payload.get("confidence"),
        detected_language=payload.get("detected_language"),
        warnings=list(payload.get("warnings", []) or []),
        metadata=dict(payload.get("metadata", {}) or {}),
    ).normalized()


def normalize_batch_requests(payloads: Sequence[Mapping[str, Any]]) -> List[TranslationRequest]:
    return [normalize_request(payload) for payload in payloads]


def normalize_batch_responses(payloads: Sequence[Mapping[str, Any]]) -> List[TranslationResponse]:
    return [normalize_response(payload) for payload in payloads]
