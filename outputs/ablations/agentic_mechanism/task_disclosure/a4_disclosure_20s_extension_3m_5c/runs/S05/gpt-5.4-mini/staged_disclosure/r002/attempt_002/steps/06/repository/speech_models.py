from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _clean_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class StreamingSpeechRequest:
    model: str
    language: Optional[str] = None
    prompt: Optional[str] = None
    temperature: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model}
        if self.language:
            payload["language"] = self.language
        if self.prompt:
            payload["prompt"] = self.prompt
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        payload.update(self.extra)
        return payload


@dataclass(frozen=True)
class StreamingSpeechWord:
    word: str
    start: Optional[float] = None
    end: Optional[float] = None
    confidence: Optional[float] = None


@dataclass(frozen=True)
class StreamingSpeechResponse:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    words: List[StreamingSpeechWord] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_word(item: Any) -> StreamingSpeechWord:
    if isinstance(item, Mapping):
        return StreamingSpeechWord(
            word=_clean_text(item.get("word") or item.get("text")),
            start=_clean_float(item.get("start") or item.get("start_time")),
            end=_clean_float(item.get("end") or item.get("end_time")),
            confidence=_clean_float(item.get("confidence")),
        )
    return StreamingSpeechWord(word=_clean_text(item))


def normalize_speech_response(payload: Mapping[str, Any]) -> StreamingSpeechResponse:
    text = _clean_text(payload.get("text") or payload.get("transcript"))
    is_final = bool(payload.get("is_final") or payload.get("final") or payload.get("message_type") == "FinalTranscript")
    confidence = _clean_float(payload.get("confidence") or payload.get("score"))
    raw_words: Sequence[Any] = payload.get("words") or payload.get("tokens") or []
    words = [normalize_word(item) for item in raw_words]
    return StreamingSpeechResponse(text=text, is_final=is_final, confidence=confidence, words=words, raw=dict(payload))


def normalize_speech_responses(payloads: Sequence[Mapping[str, Any]]) -> List[StreamingSpeechResponse]:
    return [normalize_speech_response(payload) for payload in payloads]
