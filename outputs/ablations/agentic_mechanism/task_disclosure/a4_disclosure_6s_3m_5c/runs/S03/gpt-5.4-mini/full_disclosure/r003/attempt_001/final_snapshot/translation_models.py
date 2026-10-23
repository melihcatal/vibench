from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_language_code(value: Any) -> str:
    code = _clean_text(value).replace("_", "-")
    return code.lower()


def _normalize_dictionary(data: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not data:
        return {}
    return {str(key): value for key, value in data.items()}


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = ""
    glossary_id: Optional[str] = None
    model: Optional[str] = None
    preserve_formatting: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranslationRequest":
        return TranslationRequest(
            text=_clean_text(self.text),
            source_language=_normalize_language_code(self.source_language) or None,
            target_language=_normalize_language_code(self.target_language),
            glossary_id=_clean_text(self.glossary_id) or None,
            model=_clean_text(self.model) or None,
            preserve_formatting=bool(self.preserve_formatting),
            metadata=_normalize_dictionary(self.metadata),
        )


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    model: Optional[str] = None
    detected_source_language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranslationResponse":
        return TranslationResponse(
            translated_text=_clean_text(self.translated_text),
            source_language=_normalize_language_code(self.source_language) or None,
            target_language=_normalize_language_code(self.target_language) or None,
            model=_clean_text(self.model) or None,
            detected_source_language=_normalize_language_code(self.detected_source_language) or None,
            metadata=_normalize_dictionary(self.metadata),
        )


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: Tuple[str, ...]
    source_language: Optional[str] = None
    target_language: str = ""
    glossary_id: Optional[str] = None
    model: Optional[str] = None
    preserve_formatting: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "BatchTranslationRequest":
        return BatchTranslationRequest(
            texts=tuple(_clean_text(text) for text in self.texts),
            source_language=_normalize_language_code(self.source_language) or None,
            target_language=_normalize_language_code(self.target_language),
            glossary_id=_clean_text(self.glossary_id) or None,
            model=_clean_text(self.model) or None,
            preserve_formatting=bool(self.preserve_formatting),
            metadata=_normalize_dictionary(self.metadata),
        )


@dataclass(frozen=True)
class BatchTranslationResponse:
    translations: Tuple[TranslationResponse, ...]

    def normalized(self) -> "BatchTranslationResponse":
        return BatchTranslationResponse(
            translations=tuple(item.normalized() for item in self.translations),
        )


@dataclass(frozen=True)
class TranslationQualityIssue:
    code: str
    message: str
    severity: str = "medium"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranslationQualityIssue":
        return TranslationQualityIssue(
            code=_clean_text(self.code),
            message=_clean_text(self.message),
            severity=_clean_text(self.severity).lower() or "medium",
            metadata=_normalize_dictionary(self.metadata),
        )


@dataclass(frozen=True)
class TranslationNormalizationResult:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranslationNormalizationResult":
        return TranslationNormalizationResult(
            text=_clean_text(self.text),
            language=_normalize_language_code(self.language) or None,
            metadata=_normalize_dictionary(self.metadata),
        )


def normalize_translation_request(data: Mapping[str, Any]) -> TranslationRequest:
    return TranslationRequest(
        text=_clean_text(data.get("text")),
        source_language=_normalize_language_code(data.get("source_language")) or None,
        target_language=_normalize_language_code(data.get("target_language")),
        glossary_id=_clean_text(data.get("glossary_id")) or None,
        model=_clean_text(data.get("model")) or None,
        preserve_formatting=bool(data.get("preserve_formatting", True)),
        metadata=_normalize_dictionary(data.get("metadata") if isinstance(data.get("metadata"), Mapping) else None),
    )


def normalize_batch_translation_request(data: Mapping[str, Any]) -> BatchTranslationRequest:
    raw_texts = data.get("texts") or []
    texts = tuple(_clean_text(text) for text in raw_texts if text is not None)
    return BatchTranslationRequest(
        texts=texts,
        source_language=_normalize_language_code(data.get("source_language")) or None,
        target_language=_normalize_language_code(data.get("target_language")),
        glossary_id=_clean_text(data.get("glossary_id")) or None,
        model=_clean_text(data.get("model")) or None,
        preserve_formatting=bool(data.get("preserve_formatting", True)),
        metadata=_normalize_dictionary(data.get("metadata") if isinstance(data.get("metadata"), Mapping) else None),
    )


def normalize_translation_response(data: Mapping[str, Any]) -> TranslationResponse:
    return TranslationResponse(
        translated_text=_clean_text(data.get("translated_text") or data.get("text") or data.get("translation")),
        source_language=_normalize_language_code(data.get("source_language")) or None,
        target_language=_normalize_language_code(data.get("target_language")) or None,
        model=_clean_text(data.get("model")) or None,
        detected_source_language=_normalize_language_code(data.get("detected_source_language")) or None,
        metadata=_normalize_dictionary(data.get("metadata") if isinstance(data.get("metadata"), Mapping) else None),
    )


def normalize_batch_translation_response(data: Mapping[str, Any]) -> BatchTranslationResponse:
    items = data.get("translations") or data.get("results") or []
    translations: List[TranslationResponse] = []
    for item in items:
        if isinstance(item, Mapping):
            translations.append(normalize_translation_response(item))
        else:
            translations.append(TranslationResponse(translated_text=_clean_text(item)))
    return BatchTranslationResponse(translations=tuple(translations))


def normalize_quality_issue(data: Mapping[str, Any]) -> TranslationQualityIssue:
    return TranslationQualityIssue(
        code=_clean_text(data.get("code")),
        message=_clean_text(data.get("message")),
        severity=_clean_text(data.get("severity") or "medium").lower() or "medium",
        metadata=_normalize_dictionary(data.get("metadata") if isinstance(data.get("metadata"), Mapping) else None),
    )


def normalize_quality_issues(items: Iterable[Mapping[str, Any]]) -> Tuple[TranslationQualityIssue, ...]:
    return tuple(normalize_quality_issue(item) for item in items)
