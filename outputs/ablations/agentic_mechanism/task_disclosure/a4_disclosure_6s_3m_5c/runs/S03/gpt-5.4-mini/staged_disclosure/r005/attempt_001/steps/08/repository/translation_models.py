from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def _coerce_string_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [_normalize_text(value)] if _normalize_text(value) else []
    if isinstance(value, (list, tuple)):
        result: List[str] = []
        for item in value:
            if item is None:
                continue
            text = _normalize_text(str(item))
            if text:
                result.append(text)
        return result
    text = _normalize_text(str(value))
    return [text] if text else []


@dataclass
class GeneralTextTranslationRequest:
    source_text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    glossary_terms: List[str] = field(default_factory=list)
    formality: Optional[str] = None
    preserve_formatting: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalize(self) -> "GeneralTextTranslationRequest":
        self.source_text = _normalize_text(self.source_text)
        if self.source_language is not None:
            self.source_language = _normalize_text(self.source_language)
        self.target_language = _normalize_text(self.target_language)
        self.glossary_terms = _coerce_string_list(self.glossary_terms)
        if self.formality is not None:
            self.formality = _normalize_text(self.formality)
        self.metadata = dict(self.metadata or {})
        return self

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneralTextTranslationRequest":
        return cls(
            source_text=str(data.get("source_text", "")),
            source_language=data.get("source_language"),
            target_language=str(data.get("target_language", "en")),
            glossary_terms=_coerce_string_list(data.get("glossary_terms")),
            formality=data.get("formality"),
            preserve_formatting=bool(data.get("preserve_formatting", False)),
            metadata=dict(data.get("metadata", {}) or {}),
        ).normalize()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_text": self.source_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "glossary_terms": list(self.glossary_terms),
            "formality": self.formality,
            "preserve_formatting": self.preserve_formatting,
            "metadata": dict(self.metadata),
        }


@dataclass
class GeneralTextTranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None
    target_language: Optional[str] = None
    confidence: Optional[float] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now_iso)

    def normalize(self) -> "GeneralTextTranslationResponse":
        self.translated_text = _normalize_text(self.translated_text)
        if self.detected_source_language is not None:
            self.detected_source_language = _normalize_text(self.detected_source_language)
        if self.target_language is not None:
            self.target_language = _normalize_text(self.target_language)
        if self.provider is not None:
            self.provider = _normalize_text(self.provider)
        if self.model is not None:
            self.model = _normalize_text(self.model)
        self.metadata = dict(self.metadata or {})
        return self

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneralTextTranslationResponse":
        confidence = data.get("confidence")
        if confidence is not None:
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = None
        return cls(
            translated_text=str(data.get("translated_text", "")),
            detected_source_language=data.get("detected_source_language"),
            target_language=data.get("target_language"),
            confidence=confidence,
            provider=data.get("provider"),
            model=data.get("model"),
            metadata=dict(data.get("metadata", {}) or {}),
            created_at=str(data.get("created_at", _utc_now_iso())),
        ).normalize()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "translated_text": self.translated_text,
            "detected_source_language": self.detected_source_language,
            "target_language": self.target_language,
            "confidence": self.confidence,
            "provider": self.provider,
            "model": self.model,
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }


def normalize_translation_request(data: Dict[str, Any]) -> Dict[str, Any]:
    return GeneralTextTranslationRequest.from_dict(data).to_dict()


def normalize_translation_response(data: Dict[str, Any]) -> Dict[str, Any]:
    return GeneralTextTranslationResponse.from_dict(data).to_dict()
