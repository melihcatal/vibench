from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptSegment:
    start: Optional[int]
    end: Optional[int]
    text: str
    speaker: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None


def normalize_segments(payload: Dict[str, Any]) -> List[TranscriptSegment]:
    segments = payload.get("utterances") or payload.get("segments") or []
    normalized = []
    for item in segments:
        normalized.append(TranscriptSegment(
            start=item.get("start"),
            end=item.get("end"),
            text=item.get("text", ""),
            speaker=item.get("speaker"),
            words=item.get("words"),
        ))
    return normalized
