from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Union


JsonMapping = Dict[str, Any]


def _coerce_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    if value is None:
        return default
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_dict(value: Any) -> JsonMapping:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _as_list(value: Any) -> List[Any]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return list(value)
    return []


@dataclass(slots=True)
class TranscriptWord:
    word: str = ""
    start: Optional[float] = None
    end: Optional[float] = None
    confidence: Optional[float] = None
    speaker: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptWord":
        payload = _as_dict(data)
        return cls(
            word=str(payload.get("word", payload.get("text", ""))),
            start=_coerce_float(payload.get("start")),
            end=_coerce_float(payload.get("end")),
            confidence=_coerce_float(payload.get("confidence")),
            speaker=(None if payload.get("speaker") is None else str(payload.get("speaker"))),
        )

    def to_dict(self) -> JsonMapping:
        result: JsonMapping = {"word": self.word}
        if self.start is not None:
            result["start"] = self.start
        if self.end is not None:
            result["end"] = self.end
        if self.confidence is not None:
            result["confidence"] = self.confidence
        if self.speaker is not None:
            result["speaker"] = self.speaker
        return result


@dataclass(slots=True)
class TranscriptSegment:
    text: str = ""
    start: Optional[float] = None
    end: Optional[float] = None
    confidence: Optional[float] = None
    speaker: Optional[str] = None
    words: List[TranscriptWord] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptSegment":
        payload = _as_dict(data)
        return cls(
            text=str(payload.get("text", payload.get("transcript", ""))),
            start=_coerce_float(payload.get("start")),
            end=_coerce_float(payload.get("end")),
            confidence=_coerce_float(payload.get("confidence")),
            speaker=(None if payload.get("speaker") is None else str(payload.get("speaker"))),
            words=[TranscriptWord.from_dict(item) for item in _as_list(payload.get("words"))],
        )

    def to_dict(self) -> JsonMapping:
        result: JsonMapping = {"text": self.text}
        if self.start is not None:
            result["start"] = self.start
        if self.end is not None:
            result["end"] = self.end
        if self.confidence is not None:
            result["confidence"] = self.confidence
        if self.speaker is not None:
            result["speaker"] = self.speaker
        if self.words:
            result["words"] = [word.to_dict() for word in self.words]
        return result


@dataclass(slots=True)
class BatchTranscriptionRequest:
    audio_url: Optional[str] = None
    audio_file: Optional[str] = None
    language: Optional[str] = None
    model: Optional[str] = None
    diarize: bool = False
    timestamps: bool = False
    translate_to: Optional[str] = None
    profanity_filter: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> JsonMapping:
        result: JsonMapping = dict(self.metadata)
        if self.audio_url is not None:
            result["audio_url"] = self.audio_url
        if self.audio_file is not None:
            result["audio_file"] = self.audio_file
        if self.language is not None:
            result["language"] = self.language
        if self.model is not None:
            result["model"] = self.model
        if self.diarize:
            result["diarize"] = self.diarize
        if self.timestamps:
            result["timestamps"] = self.timestamps
        if self.translate_to is not None:
            result["translate_to"] = self.translate_to
        if self.profanity_filter:
            result["profanity_filter"] = self.profanity_filter
        return result


@dataclass(slots=True)
class BatchTranscriptionResponse:
    id: Optional[str] = None
    status: str = ""
    text: str = ""
    language: Optional[str] = None
    duration: Optional[float] = None
    confidence: Optional[float] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    words: List[TranscriptWord] = field(default_factory=list)
    raw: JsonMapping = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BatchTranscriptionResponse":
        payload = _as_dict(data)
        segments = payload.get("segments") or payload.get("utterances") or []
        words = payload.get("words") or []
        text = payload.get("text", payload.get("transcript", payload.get("result", "")))
        return cls(
            id=(None if payload.get("id") is None else str(payload.get("id"))),
            status=str(payload.get("status", payload.get("state", ""))),
            text=str(text) if text is not None else "",
            language=(None if payload.get("language") is None else str(payload.get("language"))),
            duration=_coerce_float(payload.get("duration")),
            confidence=_coerce_float(payload.get("confidence")),
            segments=[TranscriptSegment.from_dict(item) for item in _as_list(segments)],
            words=[TranscriptWord.from_dict(item) for item in _as_list(words)],
            raw=payload,
        )

    def to_dict(self) -> JsonMapping:
        result: JsonMapping = dict(self.raw)
        if self.id is not None:
            result["id"] = self.id
        result["status"] = self.status
        result["text"] = self.text
        if self.language is not None:
            result["language"] = self.language
        if self.duration is not None:
            result["duration"] = self.duration
        if self.confidence is not None:
            result["confidence"] = self.confidence
        if self.segments:
            result["segments"] = [segment.to_dict() for segment in self.segments]
        if self.words:
            result["words"] = [word.to_dict() for word in self.words]
        return result


def normalize_transcript_segments(payload: Any) -> List[TranscriptSegment]:
    if isinstance(payload, BatchTranscriptionResponse):
        return list(payload.segments)
    if isinstance(payload, Mapping):
        if "segments" in payload or "utterances" in payload:
            items = payload.get("segments") or payload.get("utterances") or []
            return [TranscriptSegment.from_dict(item) for item in _as_list(items)]
        if "results" in payload:
            return [TranscriptSegment.from_dict(item) for item in _as_list(payload.get("results"))]
    return []


def normalize_transcript_text(payload: Any) -> str:
    if isinstance(payload, BatchTranscriptionResponse):
        if payload.text:
            return payload.text
        return " ".join(segment.text for segment in payload.segments if segment.text).strip()
    if isinstance(payload, Mapping):
        text = payload.get("text", payload.get("transcript", payload.get("result", "")))
        if text:
            return str(text)
        segments = normalize_transcript_segments(payload)
        return " ".join(segment.text for segment in segments if segment.text).strip()
    if isinstance(payload, str):
        return payload
    return ""


def normalize_transcript_response(payload: Any) -> BatchTranscriptionResponse:
    if isinstance(payload, BatchTranscriptionResponse):
        return payload
    if isinstance(payload, Mapping):
        return BatchTranscriptionResponse.from_dict(payload)
    return BatchTranscriptionResponse(status="", text=normalize_transcript_text(payload), raw={})


__all__ = [
    "BatchTranscriptionRequest",
    "BatchTranscriptionResponse",
    "TranscriptSegment",
    "TranscriptWord",
    "normalize_transcript_response",
    "normalize_transcript_segments",
    "normalize_transcript_text",
]
