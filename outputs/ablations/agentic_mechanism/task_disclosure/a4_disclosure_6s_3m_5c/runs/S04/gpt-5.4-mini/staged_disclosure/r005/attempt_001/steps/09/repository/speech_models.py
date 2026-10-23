from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Union


AudioSource = Union[str, bytes, Dict[str, Any]]


@dataclass
class BatchSpeechToTextRequest:
    audio_sources: Sequence[AudioSource]
    language: Optional[str] = None
    model: str = "openai/whisper-1"
    prompt: Optional[str] = None
    temperature: float = 0.0
    response_format: str = "json"
    timestamp_granularities: Sequence[str] = field(default_factory=tuple)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": self.response_format,
            "audio_sources": [normalize_audio_source(source) for source in self.audio_sources],
        }
        if self.language is not None:
            payload["language"] = self.language
        if self.prompt is not None:
            payload["prompt"] = self.prompt
        if self.timestamp_granularities:
            payload["timestamp_granularities"] = list(self.timestamp_granularities)
        return payload


@dataclass
class BatchSpeechToTextItem:
    index: int
    text: str
    language: Optional[str] = None
    duration_seconds: Optional[float] = None
    confidence: Optional[float] = None
    words: Sequence[Dict[str, Any]] = field(default_factory=tuple)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchSpeechToTextResponse:
    items: List[BatchSpeechToTextItem]
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "BatchSpeechToTextResponse":
        normalized_items = [normalize_transcription_item(item, index=i) for i, item in enumerate(data.get("items", []))]
        return cls(items=normalized_items, raw=data)


def normalize_audio_source(source: AudioSource) -> Dict[str, Any]:
    if isinstance(source, dict):
        normalized = dict(source)
        if "type" not in normalized:
            normalized["type"] = "url" if isinstance(normalized.get("url"), str) else "inline"
        return normalized
    if isinstance(source, bytes):
        return {"type": "bytes", "data": source}
    if isinstance(source, str):
        return {"type": "url", "url": source}
    raise TypeError(f"Unsupported audio source type: {type(source)!r}")


def normalize_transcription_item(item: Dict[str, Any], index: int = 0) -> BatchSpeechToTextItem:
    text = str(item.get("text", ""))
    return BatchSpeechToTextItem(
        index=index,
        text=text,
        language=item.get("language"),
        duration_seconds=_to_float(item.get("duration_seconds")),
        confidence=_to_float(item.get("confidence")),
        words=list(item.get("words", [])),
        raw=dict(item),
    )


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
