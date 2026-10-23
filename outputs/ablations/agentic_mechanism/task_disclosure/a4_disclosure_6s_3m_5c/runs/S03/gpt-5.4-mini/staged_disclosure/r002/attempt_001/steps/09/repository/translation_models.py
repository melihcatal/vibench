from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


TextLike = Union[str, Sequence[str]]


def _to_list(value: TextLike) -> List[str]:
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value]


def _compact_dict(data: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass(frozen=True)
class TranslationRequest:
    text: TextLike
    target_language: str
    source_language: Optional[str] = None
    format: Optional[str] = None
    model: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": _to_list(self.text),
            "target_language": self.target_language,
            "source_language": self.source_language,
            "format": self.format,
            "model": self.model,
        }
        if self.options:
            payload["options"] = dict(self.options)
        return _compact_dict(payload)


@dataclass(frozen=True)
class TranslationResult:
    text: str
    detected_source_language: Optional[str] = None
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "TranslationResult":
        text = payload.get("text")
        if isinstance(text, list):
            text = text[0] if text else ""
        return cls(
            text=str(text or ""),
            detected_source_language=payload.get("detected_source_language"),
            confidence=payload.get("confidence"),
            raw=dict(payload),
        )


@dataclass(frozen=True)
class TranslationResponse:
    translations: List[TranslationResult]
    model: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "TranslationResponse":
        items = payload.get("translations") or payload.get("data") or []
        translations = [
            TranslationResult.from_payload(item) if isinstance(item, Mapping) else TranslationResult(text=str(item))
            for item in items
        ]
        usage = payload.get("usage") or {}
        return cls(
            translations=translations,
            model=payload.get("model"),
            usage=dict(usage) if isinstance(usage, Mapping) else {},
            raw=dict(payload),
        )


def normalize_translation_request(data: Union[TranslationRequest, Mapping[str, Any]]) -> Dict[str, Any]:
    if isinstance(data, TranslationRequest):
        return data.normalized()
    text = data.get("text")
    if text is None:
        raise ValueError("translation request requires 'text'")
    return TranslationRequest(
        text=text,
        target_language=str(data.get("target_language") or data.get("targetLanguage") or ""),
        source_language=data.get("source_language") or data.get("sourceLanguage"),
        format=data.get("format"),
        model=data.get("model"),
        options=dict(data.get("options") or {}),
    ).normalized()


def normalize_translation_response(data: Union[TranslationResponse, Mapping[str, Any]]) -> TranslationResponse:
    if isinstance(data, TranslationResponse):
        return data
    return TranslationResponse.from_payload(data)
