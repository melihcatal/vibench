from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


@dataclass(slots=True)
class AudioChunk:
    content: bytes


@dataclass(slots=True)
class TranscriptResult:
    text: str
    is_final: bool
    stability: float = 0.0
    confidence: float = 0.0
    language_code: Optional[str] = None
    provider: str = "google_cloud_speech"
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranscriptEvent:
    results: list[TranscriptResult]
    raw: dict[str, Any] = field(default_factory=dict)


def normalize_google_streaming_response(response: Any) -> TranscriptEvent:
    raw_response = {"speech_event_type": getattr(response, "speech_event_type", None)}
    results: list[TranscriptResult] = []
    for result in getattr(response, "results", []) or []:
        alternatives = list(getattr(result, "alternatives", []) or [])
        best = alternatives[0] if alternatives else None
        results.append(
            TranscriptResult(
                text=getattr(best, "transcript", "") if best else "",
                is_final=bool(getattr(result, "is_final", False)),
                stability=float(getattr(result, "stability", 0.0) or 0.0),
                confidence=float(getattr(best, "confidence", 0.0) or 0.0)
                if best
                else 0.0,
                language_code=getattr(result, "language_code", None),
                raw={
                    "channel_tag": getattr(result, "channel_tag", None),
                    "result_end_offset": str(getattr(result, "result_end_offset", "")),
                },
            )
        )
    return TranscriptEvent(results=results, raw=raw_response)


def merge_finalized_text(results: Iterable[TranscriptResult]) -> str:
    return " ".join(
        result.text.strip()
        for result in results
        if result.is_final and result.text.strip()
    ).strip()


def merge_visible_text(results: Iterable[TranscriptResult]) -> str:
    return " ".join(
        result.text.strip() for result in results if result.text.strip()
    ).strip()
