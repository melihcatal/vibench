from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass
class StreamingConfig:
    sample_rate_hz: int = 16000
    language_code: str = "en-US"
    encoding: str = "linear16"
    interim_results: bool = True
    punctuate: bool = True
    channels: int = 1


@dataclass
class TranscriptEvent:
    transcript: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    provider: str = "deepgram"
    raw: Any = None


@dataclass
class TranscriptState:
    partial: str = ""
    finals: List[str] = field(default_factory=list)

    @property
    def full_text(self) -> str:
        segments = [segment.strip() for segment in self.finals if segment.strip()]
        if self.partial.strip():
            segments.append(self.partial.strip())
        return " ".join(segments).strip()


def normalize_deepgram_result(result: Any) -> TranscriptEvent:
    channel = getattr(result, "channel", None)
    alternatives = getattr(channel, "alternatives", None) or []
    alternative = alternatives[0] if alternatives else None
    transcript = getattr(alternative, "transcript", "") if alternative else ""
    confidence = getattr(alternative, "confidence", None) if alternative else None
    language = getattr(result, "metadata", None)
    language_code = getattr(language, "language", None) if language else None
    is_final = bool(
        getattr(result, "is_final", False) or getattr(result, "speech_final", False)
    )
    return TranscriptEvent(
        transcript=transcript or "",
        is_final=is_final,
        confidence=confidence,
        language_code=language_code,
        provider="deepgram",
        raw=result,
    )


def merge_events(events: Iterable[TranscriptEvent]) -> TranscriptState:
    state = TranscriptState()
    for event in events:
        if not event.transcript.strip():
            continue
        if event.is_final:
            state.finals.append(event.transcript.strip())
            state.partial = ""
        else:
            state.partial = event.transcript.strip()
    return state
