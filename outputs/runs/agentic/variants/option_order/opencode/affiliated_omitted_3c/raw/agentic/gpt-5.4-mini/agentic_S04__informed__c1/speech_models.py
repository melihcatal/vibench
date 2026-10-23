from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptRequest:
    audio_url: str
    speaker_labels: bool = False
    auto_chapters: bool = False
    word_boost: Optional[List[str]] = None


def normalize_segments(segments: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "start": seg.get("start"),
            "end": seg.get("end"),
            "text": seg.get("text", ""),
            "speaker": seg.get("speaker"),
        }
        for seg in segments
    ]
