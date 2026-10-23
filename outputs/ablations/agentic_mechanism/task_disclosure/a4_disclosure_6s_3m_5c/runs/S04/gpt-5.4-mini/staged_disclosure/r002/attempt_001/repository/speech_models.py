from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


def _as_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def _as_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _as_list_of_dicts(value: Any) -> List[Dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


@dataclass
class BatchSpeechToTextRequest:
    input_uris: List[str]
    model: str
    language_code: Optional[str] = None
    prompt: Optional[str] = None
    temperature: Optional[float] = None
    diarization: Optional[bool] = None
    max_alternatives: Optional[int] = None
    word_timestamps: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input_uris": list(self.input_uris), "model": self.model}
        if self.language_code is not None:
            payload["language_code"] = self.language_code
        if self.prompt is not None:
            payload["prompt"] = self.prompt
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.diarization is not None:
            payload["diarization"] = self.diarization
        if self.max_alternatives is not None:
            payload["max_alternatives"] = self.max_alternatives
        if self.word_timestamps is not None:
            payload["word_timestamps"] = self.word_timestamps
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BatchSpeechToTextRequest":
        return cls(
            input_uris=[_as_str(x) for x in data.get("input_uris", []) if _as_str(x) is not None],
            model=_as_str(data.get("model")) or "",
            language_code=_as_str(data.get("language_code")),
            prompt=_as_str(data.get("prompt")),
            temperature=_as_float(data.get("temperature")),
            diarization=data.get("diarization") if isinstance(data.get("diarization"), bool) else None,
            max_alternatives=_as_int(data.get("max_alternatives")),
            word_timestamps=data.get("word_timestamps") if isinstance(data.get("word_timestamps"), bool) else None,
            metadata=_as_dict(data.get("metadata")),
        )


@dataclass
class Word:
    word: str
    start: Optional[float] = None
    end: Optional[float] = None
    confidence: Optional[float] = None
    speaker: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"word": self.word}
        if self.start is not None:
            payload["start"] = self.start
        if self.end is not None:
            payload["end"] = self.end
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        if self.speaker is not None:
            payload["speaker"] = self.speaker
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Word":
        return cls(
            word=_as_str(data.get("word")) or "",
            start=_as_float(data.get("start")),
            end=_as_float(data.get("end")),
            confidence=_as_float(data.get("confidence")),
            speaker=_as_str(data.get("speaker")),
        )


@dataclass
class TranscriptAlternative:
    text: str
    confidence: Optional[float] = None
    words: List[Word] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text}
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        if self.words:
            payload["words"] = [word.to_dict() for word in self.words]
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptAlternative":
        return cls(
            text=_as_str(data.get("text")) or "",
            confidence=_as_float(data.get("confidence")),
            words=[Word.from_dict(item) for item in _as_list_of_dicts(data.get("words"))],
        )


@dataclass
class BatchSpeechToTextResult:
    input_uri: str
    status: str
    alternatives: List[TranscriptAlternative] = field(default_factory=list)
    language_code: Optional[str] = None
    duration_seconds: Optional[float] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input_uri": self.input_uri, "status": self.status}
        if self.alternatives:
            payload["alternatives"] = [alt.to_dict() for alt in self.alternatives]
        if self.language_code is not None:
            payload["language_code"] = self.language_code
        if self.duration_seconds is not None:
            payload["duration_seconds"] = self.duration_seconds
        if self.error is not None:
            payload["error"] = self.error
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BatchSpeechToTextResult":
        return cls(
            input_uri=_as_str(data.get("input_uri")) or "",
            status=_as_str(data.get("status")) or "",
            alternatives=[TranscriptAlternative.from_dict(item) for item in _as_list_of_dicts(data.get("alternatives"))],
            language_code=_as_str(data.get("language_code")),
            duration_seconds=_as_float(data.get("duration_seconds")),
            error=_as_str(data.get("error")),
            metadata=_as_dict(data.get("metadata")),
        )


@dataclass
class BatchSpeechToTextResponse:
    job_id: str
    status: str
    results: List[BatchSpeechToTextResult] = field(default_factory=list)
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"job_id": self.job_id, "status": self.status}
        if self.results:
            payload["results"] = [result.to_dict() for result in self.results]
        if self.created_at is not None:
            payload["created_at"] = self.created_at
        if self.completed_at is not None:
            payload["completed_at"] = self.completed_at
        if self.error is not None:
            payload["error"] = self.error
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BatchSpeechToTextResponse":
        return cls(
            job_id=_as_str(data.get("job_id")) or "",
            status=_as_str(data.get("status")) or "",
            results=[BatchSpeechToTextResult.from_dict(item) for item in _as_list_of_dicts(data.get("results"))],
            created_at=_as_str(data.get("created_at")),
            completed_at=_as_str(data.get("completed_at")),
            error=_as_str(data.get("error")),
            metadata=_as_dict(data.get("metadata")),
        )


def normalize_batch_speech_to_text_response(data: Mapping[str, Any]) -> BatchSpeechToTextResponse:
    if isinstance(data, BatchSpeechToTextResponse):
        return data
    if not isinstance(data, Mapping):
        raise TypeError("batch speech-to-text response must be a mapping")
    return BatchSpeechToTextResponse.from_dict(data)
