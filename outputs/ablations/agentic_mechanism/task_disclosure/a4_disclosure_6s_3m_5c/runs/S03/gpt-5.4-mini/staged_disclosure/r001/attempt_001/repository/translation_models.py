from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


@dataclass
class TranslationRequest:
    text: Union[str, Sequence[str]]
    source_language: Optional[str] = None
    target_language: str = "en"
    format: str = "text"
    glossary_id: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": self.text,
            "target_language": self.target_language,
            "format": self.format,
        }
        if self.source_language:
            payload["source_language"] = self.source_language
        if self.glossary_id:
            payload["glossary_id"] = self.glossary_id
        if self.options:
            payload["options"] = dict(self.options)
        return payload


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    model: Optional[str] = None
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def _first_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("translated_text", "translation", "text", "value"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                return candidate
        raise ValueError("Could not normalize translation text from mapping")
    if isinstance(value, Sequence):
        if not value:
            raise ValueError("Cannot normalize empty translation sequence")
        first = value[0]
        return _first_text(first)
    raise TypeError("Unsupported translation text type")


def normalize_translation_response(response: Any) -> TranslationResult:
    if isinstance(response, TranslationResult):
        return response

    if isinstance(response, Mapping):
        translated_text = _first_text(
            response.get("translated_text")
            or response.get("translation")
            or response.get("text")
            or response.get("data")
            or response
        )
        detected_source_language = response.get("detected_source_language") or response.get("source_language")
        model = response.get("model")
        confidence = response.get("confidence")
        return TranslationResult(
            translated_text=translated_text,
            detected_source_language=detected_source_language,
            model=model,
            confidence=confidence,
            raw=dict(response),
        )

    translated_text = _first_text(response)
    return TranslationResult(translated_text=translated_text, raw={"response": response})


def normalize_translation_requests(requests: Any) -> List[TranslationRequest]:
    if isinstance(requests, TranslationRequest):
        return [requests]
    if isinstance(requests, Mapping):
        return [TranslationRequest(**dict(requests))]
    if isinstance(requests, Sequence) and not isinstance(requests, (str, bytes, bytearray)):
        normalized: List[TranslationRequest] = []
        for request in requests:
            if isinstance(request, TranslationRequest):
                normalized.append(request)
            elif isinstance(request, Mapping):
                normalized.append(TranslationRequest(**dict(request)))
            else:
                normalized.append(TranslationRequest(text=request))
        return normalized
    return [TranslationRequest(text=requests)]
