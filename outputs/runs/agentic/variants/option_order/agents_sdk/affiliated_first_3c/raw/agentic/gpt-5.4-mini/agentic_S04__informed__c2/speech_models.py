from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SpeechRequest:
    audio_url: Optional[str] = None
    audio_path: Optional[str] = None
    transcript_id: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    word_timestamps: bool = False
    context: Optional[str] = None


@dataclass
class SpeechSegment:
    start: float
    end: float
    text: str
    speaker: Optional[str] = None
    words: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SpeechResult:
    transcript_id: Optional[str]
    status: str
    text: str
    segments: List[SpeechSegment] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_segment(segment: Any) -> SpeechSegment:
    if isinstance(segment, dict):
        return SpeechSegment(
            start=float(segment.get("start", 0.0) or 0.0),
            end=float(segment.get("end", 0.0) or 0.0),
            text=str(segment.get("text", "") or ""),
            speaker=segment.get("speaker"),
            words=list(segment.get("words", []) or []),
        )

    return SpeechSegment(
        start=float(getattr(segment, "start", 0.0) or 0.0),
        end=float(getattr(segment, "end", 0.0) or 0.0),
        text=str(getattr(segment, "text", "") or ""),
        speaker=getattr(segment, "speaker", None),
        words=list(getattr(segment, "words", []) or []),
    )


def normalize_transcript(transcript: Any) -> SpeechResult:
    segments = []
    for item in getattr(transcript, "utterances", None) or getattr(transcript, "segments", None) or []:
        segments.append(normalize_segment(item))

    metadata = {
        "id": getattr(transcript, "id", None),
        "status": getattr(transcript, "status", None),
        "language_code": getattr(transcript, "language_code", None),
        "speaker_labels": getattr(transcript, "speaker_labels", None),
    }

    return SpeechResult(
        transcript_id=getattr(transcript, "id", None),
        status=str(getattr(transcript, "status", "unknown") or "unknown"),
        text=str(getattr(transcript, "text", "") or ""),
        segments=segments,
        metadata=metadata,
    )
