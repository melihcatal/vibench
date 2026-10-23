from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_segments(
    segments: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    return [dict(segment) for segment in segments or []]


def normalize_transcript_text(text: Optional[str]) -> str:
    return (text or "").strip()


@dataclass
class TranscriptionSubmission:
    audio_uri: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    word_timestamps: bool = False


@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    transcript: str
    segments: List[Dict[str, Any]]
    raw: Dict[str, Any]
