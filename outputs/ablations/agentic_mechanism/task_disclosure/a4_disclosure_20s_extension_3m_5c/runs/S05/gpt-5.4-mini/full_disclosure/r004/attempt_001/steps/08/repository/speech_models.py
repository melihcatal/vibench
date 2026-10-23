from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass(frozen=True)
class StreamingSpeechRequest:
    audio_chunk: bytes
    language_code: Optional[str] = None
    enable_punctuation: bool = False
    sample_rate_hz: Optional[int] = None
    encoding: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_chunk": self.audio_chunk,
            "language_code": self.language_code,
            "enable_punctuation": self.enable_punctuation,
            "sample_rate_hz": self.sample_rate_hz,
            "encoding": self.encoding,
            "metadata": dict(self.metadata),
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(frozen=True)
class SpeechAlternative:
    transcript: str
    confidence: Optional[float] = None


@dataclass(frozen=True)
class StreamingSpeechResult:
    transcript: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    alternatives: Sequence[SpeechAlternative] = field(default_factory=tuple)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_transcript(text: Optional[str]) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())


def normalize_result(data: Dict[str, Any]) -> StreamingSpeechResult:
    alternatives_data = data.get("alternatives") or []
    alternatives = tuple(
        SpeechAlternative(
            transcript=normalize_transcript(item.get("transcript", "")),
            confidence=item.get("confidence"),
        )
        for item in alternatives_data
        if isinstance(item, dict)
    )

    transcript = data.get("transcript")
    if not transcript and alternatives:
        transcript = alternatives[0].transcript

    return StreamingSpeechResult(
        transcript=normalize_transcript(transcript),
        is_final=bool(data.get("is_final", False)),
        confidence=data.get("confidence"),
        language_code=data.get("language_code"),
        alternatives=alternatives,
        raw=dict(data),
    )


def merge_transcripts(parts: Sequence[str]) -> str:
    return normalize_transcript(" ".join(part for part in parts if part))


def build_request(audio_chunk: bytes, **kwargs: Any) -> StreamingSpeechRequest:
    return StreamingSpeechRequest(audio_chunk=audio_chunk, **kwargs)
