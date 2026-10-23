from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    language: str = "en-US"
    display_name: str = "batch-transcription"
    speaker_diarization: bool = False
    timestamps: bool = False


@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    text: str = ""
    segments: Optional[List[Dict[str, Any]]] = None


def normalize_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for segment in segments or []:
        normalized.append(
            {
                "speaker": segment.get("speaker", segment.get("channel", "unknown")),
                "start": segment.get("start", segment.get("offset", 0)),
                "end": segment.get("end", segment.get("duration", 0)),
                "text": segment.get("text", ""),
                "words": segment.get("words", []),
            }
        )
    return normalized
