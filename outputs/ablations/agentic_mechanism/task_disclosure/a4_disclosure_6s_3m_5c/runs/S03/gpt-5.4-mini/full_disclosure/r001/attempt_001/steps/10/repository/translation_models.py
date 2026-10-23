from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _coerce_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = _coerce_text(value)
    return text if text != "" else None


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _coerce_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def _coerce_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def _coerce_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, Sequence):
        return [_coerce_text(item) for item in value if _coerce_text(item) != ""]
    return [_coerce_text(value)]


def _coerce_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str | None = None
    target_language: str = ""
    formality: str | None = None
    context: str | None = None
    glossary: dict[str, str] = field(default_factory=dict)
    preserve_formatting: bool = True
    model: str | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranslationRequest":
        payload = _coerce_mapping(data)
        glossary = payload.get("glossary")
        return cls(
            text=_coerce_text(payload.get("text")),
            source_language=_coerce_optional_text(payload.get("source_language")),
            target_language=_coerce_text(payload.get("target_language")),
            formality=_coerce_optional_text(payload.get("formality")),
            context=_coerce_optional_text(payload.get("context")),
            glossary={_coerce_text(k): _coerce_text(v) for k, v in _coerce_mapping(glossary).items()},
            preserve_formatting=_coerce_bool(payload.get("preserve_formatting"), True),
            model=_coerce_optional_text(payload.get("model")),
        )


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    source_language: str | None = None
    target_language: str | None = None
    detected_language: str | None = None
    model: str | None = None
    confidence: float | None = None
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranslationResult":
        payload = _coerce_mapping(data)
        return cls(
            translated_text=_coerce_text(
                payload.get("translated_text", payload.get("translation", payload.get("text")))
            ),
            source_language=_coerce_optional_text(payload.get("source_language")),
            target_language=_coerce_optional_text(payload.get("target_language")),
            detected_language=_coerce_optional_text(payload.get("detected_language")),
            model=_coerce_optional_text(payload.get("model")),
            confidence=_coerce_float(payload.get("confidence"), 0.0) if payload.get("confidence") is not None else None,
            warnings=_coerce_str_list(payload.get("warnings")),
            metadata={k: v for k, v in payload.items() if k not in {
                "translated_text",
                "translation",
                "text",
                "source_language",
                "target_language",
                "detected_language",
                "model",
                "confidence",
                "warnings",
            }},
        )


@dataclass(slots=True)
class NormalizedTranslation:
    text: str
    source_language: str | None
    target_language: str | None
    model: str | None = None
    confidence: float | None = None
    warnings: tuple[str, ...] = ()
    raw: Any = None

    @classmethod
    def from_response(cls, response: TranslationResult | Mapping[str, Any] | str) -> "NormalizedTranslation":
        if isinstance(response, TranslationResult):
            return cls(
                text=response.translated_text,
                source_language=response.source_language,
                target_language=response.target_language,
                model=response.model,
                confidence=response.confidence,
                warnings=tuple(response.warnings),
                raw=response,
            )
        if isinstance(response, Mapping):
            result = TranslationResult.from_dict(response)
            return cls.from_response(result)
        text = _coerce_text(response)
        return cls(text=text, source_language=None, target_language=None, raw=response)


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: list[str]
    source_language: str | None = None
    target_language: str = ""
    formality: str | None = None
    context: str | None = None
    glossary: dict[str, str] = field(default_factory=dict)
    preserve_formatting: bool = True
    model: str | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BatchTranslationRequest":
        payload = _coerce_mapping(data)
        return cls(
            texts=_coerce_str_list(payload.get("texts")),
            source_language=_coerce_optional_text(payload.get("source_language")),
            target_language=_coerce_text(payload.get("target_language")),
            formality=_coerce_optional_text(payload.get("formality")),
            context=_coerce_optional_text(payload.get("context")),
            glossary={_coerce_text(k): _coerce_text(v) for k, v in _coerce_mapping(payload.get("glossary")).items()},
            preserve_formatting=_coerce_bool(payload.get("preserve_formatting"), True),
            model=_coerce_optional_text(payload.get("model")),
        )


@dataclass(slots=True)
class BatchTranslationResult:
    translations: list[NormalizedTranslation] = field(default_factory=list)
    source_language: str | None = None
    target_language: str | None = None
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BatchTranslationResult":
        payload = _coerce_mapping(data)
        translations = payload.get("translations")
        normalized: list[NormalizedTranslation] = []
        if isinstance(translations, Sequence) and not isinstance(translations, str):
            for item in translations:
                normalized.append(NormalizedTranslation.from_response(item))
        return cls(
            translations=normalized,
            source_language=_coerce_optional_text(payload.get("source_language")),
            target_language=_coerce_optional_text(payload.get("target_language")),
            model=_coerce_optional_text(payload.get("model")),
            metadata={k: v for k, v in payload.items() if k not in {"translations", "source_language", "target_language", "model"}},
        )
