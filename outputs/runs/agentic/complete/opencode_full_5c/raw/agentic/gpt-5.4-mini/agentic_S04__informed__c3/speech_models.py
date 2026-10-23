from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _compact_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_segments(segments: Any) -> List[Dict[str, Any]]:
    normalized = []
    for segment in segments or []:
        if isinstance(segment, dict):
            normalized.append(
                {
                    "start": segment.get("start"),
                    "end": segment.get("end"),
                    "text": _compact_text(str(segment.get("text", ""))),
                    "speaker": segment.get("speaker"),
                    "words": segment.get("words"),
                }
            )
        else:
            normalized.append({"text": _compact_text(str(segment))})
    return normalized


@dataclass
class TranscriptionRequest:
    audio_url: str
    webhook_url: Optional[str] = None
    diarization: bool = False
    timestamps: bool = False


@dataclass
class TranscriptionResponse:
    provider: str
    job_id: str
    status: str
    transcript: str = ""
    segments: Optional[List[Dict[str, Any]]] = None
