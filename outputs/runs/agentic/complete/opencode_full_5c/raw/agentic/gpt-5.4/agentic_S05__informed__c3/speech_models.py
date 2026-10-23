from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(slots=True)
class StreamingConfig:
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    encoding: str = "linear16"
    interim_results: bool = True
    enable_automatic_punctuation: bool = True
    model: str | None = None


@dataclass(slots=True)
class TranscriptAlternative:
    transcript: str
    confidence: float | None = None


@dataclass(slots=True)
class TranscriptEvent:
    text: str
    is_final: bool
    stability: float | None = None
    confidence: float | None = None
    alternatives: list[TranscriptAlternative] = field(default_factory=list)
    raw: Any = None


def pcm_chunk_to_google_request(audio_chunk: bytes) -> dict[str, bytes]:
    return {"audio_content": audio_chunk}


def normalize_google_streaming_response(response: Any) -> list[TranscriptEvent]:
    events: list[TranscriptEvent] = []
    for result in getattr(response, "results", []) or []:
        alternatives = []
        top_text = ""
        top_confidence = None
        for alt in getattr(result, "alternatives", []) or []:
            transcript = getattr(alt, "transcript", "") or ""
            confidence = getattr(alt, "confidence", None)
            alternatives.append(
                TranscriptAlternative(transcript=transcript, confidence=confidence)
            )
            if not top_text:
                top_text = transcript
                top_confidence = confidence
        if top_text:
            events.append(
                TranscriptEvent(
                    text=top_text,
                    is_final=bool(getattr(result, "is_final", False)),
                    stability=getattr(result, "stability", None),
                    confidence=top_confidence,
                    alternatives=alternatives,
                    raw=result,
                )
            )
    return events


def join_final_transcripts(events: Iterable[TranscriptEvent]) -> str:
    return " ".join(
        event.text.strip() for event in events if event.is_final and event.text.strip()
    ).strip()
