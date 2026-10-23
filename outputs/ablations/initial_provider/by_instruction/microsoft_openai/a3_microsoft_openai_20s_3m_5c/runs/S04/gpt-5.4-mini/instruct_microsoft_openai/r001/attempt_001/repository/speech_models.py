from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    speaker: Optional[str] = None


@dataclass
class TranscriptResult:
    text: str
    segments: List[TranscriptSegment]
    raw: Dict[str, Any]


def normalize_segments(payload: Dict[str, Any]) -> List[TranscriptSegment]:
    segments = []
    for item in payload.get("segments", []) or []:
        segments.append(TranscriptSegment(text=item.get("text", ""), start=item.get("start"), end=item.get("end"), speaker=item.get("speaker")))
    return segments


def normalize_transcript(payload: Dict[str, Any]) -> TranscriptResult:
    return TranscriptResult(text=payload.get("text", ""), segments=normalize_segments(payload), raw=payload)
