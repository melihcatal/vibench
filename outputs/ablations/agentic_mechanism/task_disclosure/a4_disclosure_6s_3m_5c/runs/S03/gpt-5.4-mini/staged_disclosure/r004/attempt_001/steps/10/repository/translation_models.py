from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


def _normalize_language_code(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _normalize_model_name(value: Optional[str]) -> str:
    return (value or "").strip()


@dataclass(frozen=True)
class GeneralTextTranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    mime_type: str = "text/plain"
    model: Optional[str] = None

    def normalized(self) -> "GeneralTextTranslationRequest":
        return GeneralTextTranslationRequest(
            text=_normalize_text(self.text),
            target_language=_normalize_language_code(self.target_language) or "",
            source_language=_normalize_language_code(self.source_language),
            mime_type=_normalize_text(self.mime_type) or "text/plain",
            model=_normalize_model_name(self.model) or None,
        )

    def to_provider_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "q": _normalize_text(self.text),
            "target": _normalize_language_code(self.target_language) or "",
            "format": "html" if _normalize_text(self.mime_type).lower() == "text/html" else "text",
        }
        source_language = _normalize_language_code(self.source_language)
        if source_language:
            payload["source"] = source_language
        model = _normalize_model_name(self.model)
        if model:
            payload["model"] = model
        return payload


@dataclass(frozen=True)
class GeneralTextTranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    model: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_provider_response(cls, response: Mapping[str, Any]) -> "GeneralTextTranslationResult":
        data = dict(response)
        translated_text = _normalize_text(data.get("translatedText"))
        detected_source_language = _normalize_language_code(data.get("detectedSourceLanguage"))
        model = _normalize_model_name(data.get("model")) or None
        return cls(
            translated_text=translated_text,
            detected_source_language=detected_source_language,
            model=model,
            raw=data,
        )


def normalize_general_text_translation_request(data: Mapping[str, Any]) -> GeneralTextTranslationRequest:
    return GeneralTextTranslationRequest(
        text=_normalize_text(data.get("text")),
        target_language=_normalize_language_code(data.get("target_language") or data.get("targetLanguage")) or "",
        source_language=_normalize_language_code(data.get("source_language") or data.get("sourceLanguage")),
        mime_type=_normalize_text(data.get("mime_type") or data.get("mimeType") or "text/plain") or "text/plain",
        model=_normalize_model_name(data.get("model")) or None,
    ).normalized()


def normalize_general_text_translation_response(data: Mapping[str, Any]) -> GeneralTextTranslationResult:
    translated_text = data.get("translated_text")
    if translated_text is None:
        translated_text = data.get("translatedText")
    detected_source_language = data.get("detected_source_language")
    if detected_source_language is None:
        detected_source_language = data.get("detectedSourceLanguage")
    model = data.get("model")
    if model is None:
        model = data.get("modelName")
    return GeneralTextTranslationResult(
        translated_text=_normalize_text(translated_text),
        detected_source_language=_normalize_language_code(detected_source_language),
        model=_normalize_model_name(model) or None,
        raw=dict(data),
    )


def normalize_general_text_translation_batch(requests: Sequence[Mapping[str, Any]]) -> List[GeneralTextTranslationRequest]:
    return [normalize_general_text_translation_request(item) for item in requests]
