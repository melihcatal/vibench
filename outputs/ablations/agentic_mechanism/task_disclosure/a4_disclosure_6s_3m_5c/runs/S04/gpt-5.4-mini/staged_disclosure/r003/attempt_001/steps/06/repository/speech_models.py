from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


def _normalize_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text or None
    text = str(value).strip()
    return text or None


def _normalize_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "1", "yes", "y", "on"}:
            return True
        if text in {"false", "0", "no", "n", "off"}:
            return False
        return None
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def _normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        items = value
    else:
        items = [value]
    normalized: List[str] = []
    for item in items:
        text = _normalize_str(item)
        if text is not None:
            normalized.append(text)
    return normalized


@dataclass(frozen=True)
class BatchSpeechToTextRequest:
    audio_url: str
    language_code: Optional[str] = None
    speech_model: Optional[str] = None
    speaker_labels: Optional[bool] = None
    punctuate: Optional[bool] = None
    format_text: Optional[bool] = None
    dual_channel: Optional[bool] = None
    profanity_filter: Optional[bool] = None
    word_boost: List[str] = field(default_factory=list)
    custom_spelling: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"audio_url": self.audio_url}
        if self.language_code is not None:
            payload["language_code"] = self.language_code
        if self.speech_model is not None:
            payload["speech_model"] = self.speech_model
        if self.speaker_labels is not None:
            payload["speaker_labels"] = self.speaker_labels
        if self.punctuate is not None:
            payload["punctuate"] = self.punctuate
        if self.format_text is not None:
            payload["format_text"] = self.format_text
        if self.dual_channel is not None:
            payload["dual_channel"] = self.dual_channel
        if self.profanity_filter is not None:
            payload["profanity_filter"] = self.profanity_filter
        if self.word_boost:
            payload["word_boost"] = self.word_boost
        if self.custom_spelling:
            payload["custom_spelling"] = self.custom_spelling
        payload.update(self.metadata)
        return payload

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "BatchSpeechToTextRequest":
        return cls(
            audio_url=_normalize_str(data.get("audio_url")) or "",
            language_code=_normalize_str(data.get("language_code")),
            speech_model=_normalize_str(data.get("speech_model")),
            speaker_labels=_normalize_bool(data.get("speaker_labels")),
            punctuate=_normalize_bool(data.get("punctuate")),
            format_text=_normalize_bool(data.get("format_text")),
            dual_channel=_normalize_bool(data.get("dual_channel")),
            profanity_filter=_normalize_bool(data.get("profanity_filter")),
            word_boost=_normalize_list(data.get("word_boost")),
            custom_spelling=_normalize_list(data.get("custom_spelling")),
            metadata={k: v for k, v in data.items() if k not in {"audio_url", "language_code", "speech_model", "speaker_labels", "punctuate", "format_text", "dual_channel", "profanity_filter", "word_boost", "custom_spelling"}},
        )


@dataclass(frozen=True)
class BatchSpeechToTextResponse:
    id: Optional[str] = None
    status: Optional[str] = None
    text: Optional[str] = None
    error: Optional[str] = None
    language_code: Optional[str] = None
    duration: Optional[float] = None
    words: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "BatchSpeechToTextResponse":
        return cls(
            id=_normalize_str(data.get("id")),
            status=_normalize_str(data.get("status")),
            text=_normalize_str(data.get("text")),
            error=_normalize_str(data.get("error")),
            language_code=_normalize_str(data.get("language_code")),
            duration=_normalize_float(data.get("duration")),
            words=list(data.get("words") or []),
            raw=dict(data),
        )


def normalize_batch_speech_request(data: Mapping[str, Any]) -> Dict[str, Any]:
    request = BatchSpeechToTextRequest.from_mapping(data)
    return request.to_payload()


def normalize_batch_speech_response(data: Mapping[str, Any]) -> BatchSpeechToTextResponse:
    return BatchSpeechToTextResponse.from_mapping(data)
