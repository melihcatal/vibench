from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


def _normalize_language_code(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _normalize_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    return normalized


def _normalize_list(values: Optional[Sequence[str]]) -> List[str]:
    if not values:
        return []
    return [item for item in values if item is not None and item != ""]


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    tone: Optional[str] = None
    glossary_id: Optional[str] = None
    preserve_formatting: bool = True
    context: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranslationRequest":
        return TranslationRequest(
            text=_normalize_text(self.text) or "",
            source_language=_normalize_language_code(self.source_language),
            target_language=_normalize_language_code(self.target_language),
            tone=(self.tone.strip() if self.tone else None),
            glossary_id=(self.glossary_id.strip() if self.glossary_id else None),
            preserve_formatting=bool(self.preserve_formatting),
            context=_normalize_text(self.context),
            metadata=dict(self.metadata),
        )

    def to_payload(self) -> Dict[str, Any]:
        normalized = self.normalized()
        payload: Dict[str, Any] = {
            "text": normalized.text,
            "preserve_formatting": normalized.preserve_formatting,
        }
        if normalized.source_language is not None:
            payload["source_language"] = normalized.source_language
        if normalized.target_language is not None:
            payload["target_language"] = normalized.target_language
        if normalized.tone is not None:
            payload["tone"] = normalized.tone
        if normalized.glossary_id is not None:
            payload["glossary_id"] = normalized.glossary_id
        if normalized.context is not None:
            payload["context"] = normalized.context
        if normalized.metadata:
            payload["metadata"] = dict(normalized.metadata)
        return payload


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    detected_language: Optional[str] = None
    confidence: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "TranslationResponse":
        return cls(
            translated_text=_normalize_text(str(payload.get("translated_text", ""))) or "",
            source_language=_normalize_language_code(payload.get("source_language")),
            target_language=_normalize_language_code(payload.get("target_language")),
            detected_language=_normalize_language_code(payload.get("detected_language")),
            confidence=payload.get("confidence"),
            warnings=_normalize_list(payload.get("warnings")),
            metadata=dict(payload.get("metadata") or {}),
        )

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "translated_text": self.translated_text,
            "warnings": list(self.warnings),
        }
        if self.source_language is not None:
            payload["source_language"] = self.source_language
        if self.target_language is not None:
            payload["target_language"] = self.target_language
        if self.detected_language is not None:
            payload["detected_language"] = self.detected_language
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class NormalizedTranslation:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    normalization_notes: List[str] = field(default_factory=list)

    @classmethod
    def from_texts(
        cls,
        source_text: str,
        translated_text: str,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
        normalization_notes: Optional[Sequence[str]] = None,
    ) -> "NormalizedTranslation":
        return cls(
            source_text=_normalize_text(source_text) or "",
            translated_text=_normalize_text(translated_text) or "",
            source_language=_normalize_language_code(source_language),
            target_language=_normalize_language_code(target_language),
            normalization_notes=_normalize_list(normalization_notes),
        )

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "normalization_notes": list(self.normalization_notes),
        }
        if self.source_language is not None:
            payload["source_language"] = self.source_language
        if self.target_language is not None:
            payload["target_language"] = self.target_language
        return payload
