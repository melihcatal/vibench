from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StreamingConfig:
    sample_rate: int = 16000
    channels: int = 1
    encoding: str = "linear16"
    language: str = "en-US"
    interim_results: bool = True
    punctuate: bool = True
    endpointing_ms: int = 300
    utterance_end_ms: int = 1000
    model: str = "nova-2"


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    is_final: bool = False
    confidence: float | None = None
    start: float | None = None
    end: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranscriptEvent:
    segments: list[TranscriptSegment]
    speech_final: bool = False
    utterance_final: bool = False
    request_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return " ".join(
            segment.text for segment in self.segments if segment.text
        ).strip()


def normalize_transcript_event(payload: Any) -> TranscriptEvent:
    if payload is None:
        return TranscriptEvent(segments=[], raw={})

    if isinstance(payload, TranscriptEvent):
        return payload

    if hasattr(payload, "to_dict"):
        payload = payload.to_dict()
    elif not isinstance(payload, dict):
        payload = dict(payload)

    channel = (payload.get("channel") or {}) if isinstance(payload, dict) else {}
    alternatives = channel.get("alternatives") or []
    segments: list[TranscriptSegment] = []
    for alternative in alternatives:
        transcript = (alternative.get("transcript") or "").strip()
        if not transcript:
            continue
        words = alternative.get("words") or []
        start = words[0].get("start") if words else None
        end = words[-1].get("end") if words else None
        segments.append(
            TranscriptSegment(
                text=transcript,
                is_final=bool(payload.get("is_final") or payload.get("speech_final")),
                confidence=alternative.get("confidence"),
                start=start,
                end=end,
                raw=alternative,
            )
        )

    return TranscriptEvent(
        segments=segments,
        speech_final=bool(payload.get("speech_final")),
        utterance_final=bool(payload.get("from_finalize") or payload.get("is_final")),
        request_id=payload.get("metadata", {}).get("request_id")
        if isinstance(payload.get("metadata"), dict)
        else None,
        raw=payload,
    )


def merge_transcript_text(events: list[TranscriptEvent]) -> str:
    return "\n".join(event.text for event in events if event.text).strip()


def normalize_caption_chunk(text: str) -> str:
    return " ".join((text or "").split()).strip()
