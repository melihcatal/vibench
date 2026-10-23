from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str
    speaker: Optional[str] = None
    words: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranscriptionJobRequest:
    audio_path: str
    model: str
    language: Optional[str] = None
    prompt: Optional[str] = None
    speaker_diarization: bool = False
    response_format: str = "verbose_json"
    include: Optional[List[str]] = None


@dataclass
class TranscriptionJobResponse:
    job_id: str
    status: str
    transcript: Optional[str] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_segments(raw_segments: Iterable[Dict[str, Any]]) -> List[TranscriptSegment]:
    normalized: List[TranscriptSegment] = []
    for seg in raw_segments or []:
        normalized.append(
            TranscriptSegment(
                start=float(seg.get("start", 0.0)),
                end=float(seg.get("end", 0.0)),
                text=str(seg.get("text", "")).strip(),
                speaker=seg.get("speaker") or seg.get("speaker_id"),
                words=list(seg.get("words", [])) if seg.get("words") else [],
            )
        )
    return normalized
