from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass
class StreamingOptions:
    language_code: str = "en-US"
    interim_results: bool = True
    punctuate: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "linear16"
    channels: int = 1
    model: str = "nova-2"


@dataclass
class TranscriptAlternative:
    transcript: str
    confidence: Optional[float] = None


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    start: Optional[float] = None
    end: Optional[float] = None
    channel_index: int = 0
    alternatives: List[TranscriptAlternative] = field(default_factory=list)
    raw: Any = None


def normalize_deepgram_result(result: Any) -> TranscriptEvent:
    channel = getattr(result, "channel", None)
    alternative_items = []
    primary_text = ""
    primary_confidence = None
    if channel and getattr(channel, "alternatives", None):
        for alt in channel.alternatives:
            alternative_items.append(
                TranscriptAlternative(
                    transcript=getattr(alt, "transcript", "") or "",
                    confidence=getattr(alt, "confidence", None),
                )
            )
        if alternative_items:
            primary_text = alternative_items[0].transcript
            primary_confidence = alternative_items[0].confidence
    return TranscriptEvent(
        text=primary_text,
        is_final=bool(getattr(result, "is_final", False)),
        confidence=primary_confidence,
        start=getattr(result, "start", None),
        end=getattr(result, "duration", None),
        channel_index=getattr(channel, "index", 0) if channel else 0,
        alternatives=alternative_items,
        raw=result,
    )


def join_final_transcripts(events: Iterable[TranscriptEvent]) -> str:
    return " ".join(
        event.text.strip() for event in events if event.is_final and event.text.strip()
    )
