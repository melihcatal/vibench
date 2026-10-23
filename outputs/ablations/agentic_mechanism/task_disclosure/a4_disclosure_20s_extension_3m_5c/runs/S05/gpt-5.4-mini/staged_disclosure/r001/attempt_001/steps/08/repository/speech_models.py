from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass(frozen=True)
class StreamingSpeechRequest:
    audio: bytes
    sample_rate: int = 16000
    language: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"
    prompt: Optional[str] = None
    vad: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "sample_rate": self.sample_rate,
            "model": self.model,
            "vad": self.vad,
        }
        if self.language:
            payload["language"] = self.language
        if self.prompt:
            payload["prompt"] = self.prompt
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class TranscriptAlternative:
    text: str = ""
    confidence: Optional[float] = None

    @classmethod
    def from_any(cls, value: Any) -> "TranscriptAlternative":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(text=value)
        if isinstance(value, Mapping):
            return cls(
                text=str(value.get("text", "")),
                confidence=value.get("confidence"),
            )
        return cls(text=str(value))


@dataclass(frozen=True)
class StreamingSpeechResponse:
    text: str = ""
    is_final: bool = False
    language: Optional[str] = None
    confidence: Optional[float] = None
    alternatives: List[TranscriptAlternative] = field(default_factory=list)
    raw: Optional[Mapping[str, Any]] = None

    @classmethod
    def normalize(cls, value: Any) -> "StreamingSpeechResponse":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(text=value)
        if not isinstance(value, Mapping):
            return cls(text=str(value))

        alternatives = value.get("alternatives") or value.get("results") or []
        normalized_alternatives = [TranscriptAlternative.from_any(item) for item in alternatives if item is not None]

        text = value.get("text") or value.get("transcript") or ""
        if not text and normalized_alternatives:
            text = normalized_alternatives[0].text

        return cls(
            text=str(text),
            is_final=bool(value.get("is_final", value.get("final", False))),
            language=value.get("language"),
            confidence=value.get("confidence"),
            alternatives=normalized_alternatives,
            raw=value,
        )


def normalize_streaming_speech_response(value: Any) -> StreamingSpeechResponse:
    return StreamingSpeechResponse.normalize(value)


def normalize_streaming_speech_responses(values: Any) -> List[StreamingSpeechResponse]:
    if values is None:
        return []
    if isinstance(values, (str, bytes)):
        return [StreamingSpeechResponse.normalize(values)]
    if isinstance(values, Mapping):
        return [StreamingSpeechResponse.normalize(values)]
    return [StreamingSpeechResponse.normalize(item) for item in values]


__all__ = [
    "StreamingSpeechRequest",
    "StreamingSpeechResponse",
    "TranscriptAlternative",
    "normalize_streaming_speech_response",
    "normalize_streaming_speech_responses",
]
