from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


def _as_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    if hasattr(value, "dict"):
        return dict(value.dict())
    raise TypeError("Expected mapping-like value")


def _normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


def _normalize_confidence(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_list(value: Any) -> List[Dict[str, Any]]:
    if not value:
        return []
    items = value if isinstance(value, list) else list(value)
    normalized: List[Dict[str, Any]] = []
    for item in items:
        normalized.append(_as_dict(item))
    return normalized


@dataclass(frozen=True)
class TranscriptionRequest:
    audio_url: str
    language_code: Optional[str] = None
    punctuate: Optional[bool] = None
    format_text: Optional[bool] = None
    speaker_labels: Optional[bool] = None
    sentiment_analysis: Optional[bool] = None
    entity_detection: Optional[bool] = None
    auto_highlights: Optional[bool] = None
    multichannel: Optional[bool] = None
    dual_channel: Optional[bool] = None
    webhook_url: Optional[str] = None
    webhook_auth_header_name: Optional[str] = None
    webhook_auth_header_value: Optional[str] = None
    extra: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"audio_url": self.audio_url}
        for key, value in (
            ("language_code", self.language_code),
            ("punctuate", self.punctuate),
            ("format_text", self.format_text),
            ("speaker_labels", self.speaker_labels),
            ("sentiment_analysis", self.sentiment_analysis),
            ("entity_detection", self.entity_detection),
            ("auto_highlights", self.auto_highlights),
            ("multichannel", self.multichannel),
            ("dual_channel", self.dual_channel),
            ("webhook_url", self.webhook_url),
            ("webhook_auth_header_name", self.webhook_auth_header_name),
            ("webhook_auth_header_value", self.webhook_auth_header_value),
        ):
            if value is not None:
                payload[key] = value
        payload.update(dict(self.extra))
        return payload


@dataclass(frozen=True)
class WordTimestamp:
    word: str
    start: Optional[float] = None
    end: Optional[float] = None
    confidence: Optional[float] = None
    speaker: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WordTimestamp":
        return cls(
            word=_normalize_text(data.get("word")),
            start=data.get("start"),
            end=data.get("end"),
            confidence=_normalize_confidence(data.get("confidence")),
            speaker=data.get("speaker"),
        )


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    words: Sequence[WordTimestamp] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptSegment":
        words = tuple(WordTimestamp.from_dict(item) for item in _normalize_list(data.get("words")))
        return cls(
            text=_normalize_text(data.get("text")),
            start=data.get("start"),
            end=data.get("end"),
            speaker=data.get("speaker"),
            confidence=_normalize_confidence(data.get("confidence")),
            words=words,
        )


@dataclass(frozen=True)
class TranscriptionResult:
    id: str
    status: str
    text: str = ""
    audio_url: Optional[str] = None
    language_code: Optional[str] = None
    confidence: Optional[float] = None
    duration: Optional[float] = None
    utterances: Sequence[TranscriptSegment] = field(default_factory=tuple)
    paragraphs: Sequence[TranscriptSegment] = field(default_factory=tuple)
    words: Sequence[WordTimestamp] = field(default_factory=tuple)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptionResult":
        payload = _as_dict(data)
        return cls(
            id=str(payload.get("id", "")),
            status=str(payload.get("status", "")),
            text=_normalize_text(payload.get("text")),
            audio_url=payload.get("audio_url"),
            language_code=payload.get("language_code"),
            confidence=_normalize_confidence(payload.get("confidence")),
            duration=payload.get("duration"),
            utterances=tuple(TranscriptSegment.from_dict(item) for item in _normalize_list(payload.get("utterances"))),
            paragraphs=tuple(TranscriptSegment.from_dict(item) for item in _normalize_list(payload.get("paragraphs"))),
            words=tuple(WordTimestamp.from_dict(item) for item in _normalize_list(payload.get("words"))),
            raw=payload,
        )


def normalize_transcript_result(data: Mapping[str, Any]) -> TranscriptionResult:
    return TranscriptionResult.from_dict(data)


def normalize_transcript_segments(data: Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]) -> List[TranscriptSegment]:
    if isinstance(data, Mapping):
        values = data.get("segments") or data.get("utterances") or data.get("paragraphs") or []
    else:
        values = data
    return [TranscriptSegment.from_dict(item) for item in values]


def build_transcription_request(audio_url: str, **kwargs: Any) -> TranscriptionRequest:
    extra = kwargs.pop("extra", {})
    return TranscriptionRequest(audio_url=audio_url, extra=extra, **kwargs)
