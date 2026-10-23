from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptRequest:
    audio_path: str
    language: Optional[str] = None
    diarize: bool = False
    timestamp_granularity: Optional[str] = None


def normalize_segments(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = data.get("segments") or data.get("transcript", {}).get("segments") or []
    normalized = []
    for segment in segments:
        normalized.append(
            {
                "start": segment.get("start"),
                "end": segment.get("end"),
                "speaker": segment.get("speaker") or segment.get("speaker_id"),
                "text": segment.get("text", ""),
                "words": segment.get("words", []),
            }
        )
    return normalized


def normalize_transcript_text(data: Dict[str, Any]) -> str:
    if isinstance(data.get("text"), str):
        return data["text"]
    return data.get("transcript", {}).get("text", "")
