from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text).strip()


def normalize_segments(segments: Any) -> List[Dict[str, Any]]:
    if not segments:
        return []
    normalized = []
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        normalized.append({
            "start": segment.get("start"),
            "end": segment.get("end"),
            "speaker": segment.get("speaker"),
            "text": normalize_text(segment.get("text")),
            "words": segment.get("words") or [],
        })
    return normalized


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: str = "en-US"
    speaker_labels: bool = False
    timestamps: bool = False


@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    transcript: str
    segments: List[Dict[str, Any]]
    raw: Dict[str, Any]
