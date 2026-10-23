from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionSubmitRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None
    word_timestamps: bool = False


@dataclass
class TranscriptStatus:
    transcript_id: str
    status: str
    error: Optional[str] = None


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    words: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranscriptResult:
    transcript_id: str
    status: str
    text: str
    language_code: Optional[str] = None
    confidence: Optional[float] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    utterances: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_utterance(item: Dict[str, Any]) -> TranscriptSegment:
    return TranscriptSegment(
        text=item.get("text", ""),
        start_ms=item.get("start"),
        end_ms=item.get("end"),
        speaker=item.get("speaker"),
        confidence=item.get("confidence"),
        words=item.get("words") or [],
    )


def normalize_transcript_response(payload: Dict[str, Any]) -> TranscriptResult:
    utterances = [
        normalize_utterance(item) for item in (payload.get("utterances") or [])
    ]
    words = payload.get("words") or []
    segments = []
    if utterances:
        segments = utterances
    elif words:
        for word in words:
            segments.append(
                TranscriptSegment(
                    text=word.get("text") or word.get("word") or "",
                    start_ms=word.get("start"),
                    end_ms=word.get("end"),
                    confidence=word.get("confidence"),
                    words=[word],
                )
            )
    return TranscriptResult(
        transcript_id=payload.get("id", ""),
        status=payload.get("status", ""),
        text=payload.get("text", ""),
        language_code=payload.get("language_code"),
        confidence=payload.get("confidence"),
        segments=segments,
        utterances=utterances,
        raw=payload,
    )
