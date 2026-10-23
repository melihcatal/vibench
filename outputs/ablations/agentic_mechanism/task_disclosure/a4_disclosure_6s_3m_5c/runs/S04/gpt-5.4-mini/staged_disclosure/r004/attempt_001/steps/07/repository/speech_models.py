from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass(frozen=True)
class BatchSpeechRequest:
    audio_url: str
    language_code: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"
    prompt: Optional[str] = None
    format: Optional[str] = None
    extras: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"audio_url": self.audio_url, "model": self.model}
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.prompt:
            payload["prompt"] = self.prompt
        if self.format:
            payload["format"] = self.format
        payload.update(self.extras)
        return payload


@dataclass(frozen=True)
class BatchSpeechWord:
    word: str
    start: Optional[float] = None
    end: Optional[float] = None
    confidence: Optional[float] = None


@dataclass(frozen=True)
class BatchSpeechSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    words: List[BatchSpeechWord] = field(default_factory=list)
    speaker: Optional[str] = None


@dataclass(frozen=True)
class BatchSpeechResponse:
    text: str
    language_code: Optional[str] = None
    duration: Optional[float] = None
    segments: List[BatchSpeechSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def _as_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_word(data: Mapping[str, Any]) -> BatchSpeechWord:
    return BatchSpeechWord(
        word=str(data.get("word", data.get("text", ""))),
        start=_as_float(data.get("start")),
        end=_as_float(data.get("end")),
        confidence=_as_float(data.get("confidence")),
    )


def _normalize_segment(data: Mapping[str, Any]) -> BatchSpeechSegment:
    words_data = data.get("words") or []
    words = [_normalize_word(word) for word in words_data if isinstance(word, Mapping)]
    return BatchSpeechSegment(
        text=str(data.get("text", "")),
        start=_as_float(data.get("start")),
        end=_as_float(data.get("end")),
        words=words,
        speaker=data.get("speaker"),
    )


def normalize_batch_speech_response(data: Mapping[str, Any]) -> BatchSpeechResponse:
    segments_data = data.get("segments") or data.get("utterances") or []
    segments = [_normalize_segment(segment) for segment in segments_data if isinstance(segment, Mapping)]
    text = str(data.get("text", "")).strip()
    if not text and segments:
        text = " ".join(segment.text for segment in segments if segment.text).strip()
    return BatchSpeechResponse(
        text=text,
        language_code=data.get("language_code") or data.get("language"),
        duration=_as_float(data.get("duration")),
        segments=segments,
        raw=dict(data),
    )
