from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_segments(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = data.get("segments") or data.get("response", {}).get("body", {}).get("segments") or []
    return [
        {
            "id": seg.get("id"),
            "start": seg.get("start"),
            "end": seg.get("end"),
            "text": seg.get("text", ""),
            "speaker": seg.get("speaker"),
            "words": seg.get("words", []),
        }
        for seg in segments
    ]


def normalize_transcript_text(data: Dict[str, Any]) -> str:
    if isinstance(data.get("text"), str):
        return data["text"]
    return " ".join(segment["text"] for segment in normalize_segments(data) if segment["text"])


@dataclass
class TranscriptJobRef:
    id: str
    status: Optional[str] = None
