from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _compact_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    return " ".join(str(value).split())


def normalize_segments(segments: Any) -> List[Dict[str, Any]]:
    normalized = []
    for segment in segments or []:
        if isinstance(segment, dict):
            normalized.append(
                {
                    "start": segment.get("start"),
                    "end": segment.get("end"),
                    "speaker": segment.get("speaker"),
                    "text": _compact_text(segment.get("text")),
                    "words": segment.get("words"),
                }
            )
        else:
            normalized.append({"text": _compact_text(segment)})
    return normalized


def normalize_transcript(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "job_id": payload.get("job_id")
        or payload.get("id")
        or payload.get("transcript_id"),
        "status": payload.get("status"),
        "text": _compact_text(
            payload.get("text") or payload.get("transcript") or payload.get("full_text")
        ),
        "segments": normalize_segments(
            payload.get("segments") or payload.get("utterances") or payload.get("items")
        ),
        "words": payload.get("words") or payload.get("word_timestamps") or [],
        "source": payload,
    }


@dataclass
class TranscriptionJob:
    job_id: str
    status: Optional[str] = None
    transcript_url: Optional[str] = None


@dataclass
class TranscriptResult:
    job_id: Optional[str]
    status: Optional[str]
    text: str
    segments: List[Dict[str, Any]]
    words: List[Dict[str, Any]]
    source: Dict[str, Any]
