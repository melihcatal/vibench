from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class SpeechEventType(str, Enum):
    START = "start"
    AUDIO = "audio"
    END = "end"
    RESULT = "result"
    ERROR = "error"


@dataclass
class StreamingSpeechRequest:
    event_type: SpeechEventType
    audio: Optional[bytes] = None
    sample_rate_hz: Optional[int] = None
    language: Optional[str] = None
    format: Optional[str] = None
    enable_partials: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "type": self.event_type.value,
            "enable_partials": self.enable_partials,
            "metadata": self.metadata,
        }
        if self.audio is not None:
            payload["audio"] = self.audio
        if self.sample_rate_hz is not None:
            payload["sample_rate_hz"] = self.sample_rate_hz
        if self.language is not None:
            payload["language"] = self.language
        if self.format is not None:
            payload["format"] = self.format
        return payload


@dataclass
class SpeechAlternative:
    transcript: str
    confidence: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpeechAlternative":
        return cls(
            transcript=str(data.get("transcript", "")),
            confidence=data.get("confidence"),
        )


@dataclass
class StreamingSpeechResponse:
    event_type: SpeechEventType
    transcript: str = ""
    is_final: bool = False
    language: Optional[str] = None
    alternatives: List[SpeechAlternative] = field(default_factory=list)
    error: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamingSpeechResponse":
        event = str(data.get("type", SpeechEventType.RESULT.value))
        alternatives_data = data.get("alternatives") or []
        alternatives = [
            alt if isinstance(alt, SpeechAlternative) else SpeechAlternative.from_dict(alt)
            for alt in alternatives_data
            if isinstance(alt, dict)
        ]
        transcript = str(data.get("transcript", ""))
        if not transcript and alternatives:
            transcript = alternatives[0].transcript
        return cls(
            event_type=SpeechEventType(event) if event in SpeechEventType._value2member_map_ else SpeechEventType.RESULT,
            transcript=transcript,
            is_final=bool(data.get("is_final", False)),
            language=data.get("language"),
            alternatives=alternatives,
            error=data.get("error"),
            raw=dict(data),
        )


def normalize_streaming_speech_event(event: Union[StreamingSpeechRequest, StreamingSpeechResponse, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(event, StreamingSpeechRequest):
        return event.to_dict()
    if isinstance(event, StreamingSpeechResponse):
        return {
            "type": event.event_type.value,
            "transcript": event.transcript,
            "is_final": event.is_final,
            "language": event.language,
            "alternatives": [
                {"transcript": alt.transcript, "confidence": alt.confidence}
                for alt in event.alternatives
            ],
            "error": event.error,
            "raw": event.raw,
        }
    if isinstance(event, dict):
        return dict(event)
    raise TypeError("Unsupported streaming speech event type")
