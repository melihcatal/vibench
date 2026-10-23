from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BatchTranscriptionRequest:
    audio_url: str
    language_code: str = "en"
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    speaker: str | None = None
    start: float | None = None
    end: float | None = None
    words: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class BatchTranscriptionResult:
    transcript_id: str
    status: str
    text: str
    audio_url: str | None = None
    language_code: str | None = None
    confidence: float | None = None
    segments: list[TranscriptSegment] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


def normalize_assemblyai_transcript(payload: Any) -> BatchTranscriptionResult:
    transcript_id = getattr(payload, "id", None) or payload.get("id", "")
    status = getattr(payload, "status", None) or payload.get("status", "")
    text = getattr(payload, "text", None) or payload.get("text", "") or ""
    audio_url = getattr(payload, "audio_url", None) or payload.get("audio_url")
    language_code = getattr(payload, "language_code", None) or payload.get(
        "language_code"
    )
    confidence = getattr(payload, "confidence", None) or payload.get("confidence")
    utterances = getattr(payload, "utterances", None) or payload.get("utterances") or []
    words = getattr(payload, "words", None) or payload.get("words") or []
    segments: list[TranscriptSegment] = []
    if utterances:
        for utterance in utterances:
            source = utterance if isinstance(utterance, dict) else utterance.__dict__
            segments.append(
                TranscriptSegment(
                    text=source.get("text", ""),
                    speaker=source.get("speaker"),
                    start=_ms_to_seconds(source.get("start")),
                    end=_ms_to_seconds(source.get("end")),
                    words=source.get("words") or [],
                )
            )
    elif words:
        segments.append(
            TranscriptSegment(
                text=text,
                start=_ms_to_seconds(words[0].get("start")) if words else None,
                end=_ms_to_seconds(words[-1].get("end")) if words else None,
                words=words,
            )
        )
    raw = payload if isinstance(payload, dict) else payload.__dict__
    return BatchTranscriptionResult(
        transcript_id=transcript_id,
        status=status,
        text=text,
        audio_url=audio_url,
        language_code=language_code,
        confidence=confidence,
        segments=segments,
        raw=raw,
    )


def _ms_to_seconds(value: Any) -> float | None:
    if value is None:
        return None
    return round(float(value) / 1000.0, 3)
