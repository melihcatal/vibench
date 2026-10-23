from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


@dataclass
class TranslationRequest:
    text: Union[str, List[str]]
    source_language: Optional[str] = None
    target_language: str = "en"
    formality: Optional[str] = None
    glossary_id: Optional[str] = None
    preserve_formatting: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": self.text,
            "target_language": self.target_language,
            "preserve_formatting": self.preserve_formatting,
        }
        if self.source_language is not None:
            payload["source_language"] = self.source_language
        if self.formality is not None:
            payload["formality"] = self.formality
        if self.glossary_id is not None:
            payload["glossary_id"] = self.glossary_id
        payload.update(self.extra)
        return payload


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    confidence: Optional[float] = None
    model: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResponse:
    translations: List[TranslationResult]
    request_id: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def _coerce_translation_result(item: Any) -> TranslationResult:
    if isinstance(item, TranslationResult):
        return item
    if isinstance(item, str):
        return TranslationResult(translated_text=item, raw={"translated_text": item})
    if isinstance(item, dict):
        translated_text = item.get("translated_text") or item.get("text") or item.get("translation") or ""
        return TranslationResult(
            translated_text=translated_text,
            detected_source_language=item.get("detected_source_language") or item.get("source_language"),
            confidence=item.get("confidence"),
            model=item.get("model"),
            raw=dict(item),
        )
    return TranslationResult(translated_text=str(item), raw={"value": item})


def normalize_translation_response(payload: Any) -> TranslationResponse:
    if isinstance(payload, TranslationResponse):
        return payload

    if isinstance(payload, dict):
        translations_value = (
            payload.get("translations")
            or payload.get("data")
            or payload.get("results")
            or payload.get("translation")
            or payload.get("translated_text")
        )

        if translations_value is None:
            translations = []
        elif isinstance(translations_value, list):
            translations = [_coerce_translation_result(item) for item in translations_value]
        else:
            translations = [_coerce_translation_result(translations_value)]

        request_id = payload.get("request_id") or payload.get("id") or payload.get("job_id")
        return TranslationResponse(translations=translations, request_id=request_id, raw=dict(payload))

    if isinstance(payload, list):
        return TranslationResponse(translations=[_coerce_translation_result(item) for item in payload], raw={"data": payload})

    return TranslationResponse(translations=[_coerce_translation_result(payload)], raw={"value": payload})
