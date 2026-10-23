from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptSegment:
    index: int
    start: Optional[float]
    end: Optional[float]
    text: str
    speaker: Optional[str] = None


@dataclass
class TranscriptResult:
    text: str
    segments: List[TranscriptSegment]
    raw: Any


def normalize_segments(payload: Any) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    if isinstance(payload, dict):
        items = payload.get("segments") or payload.get("words") or []
    else:
        items = payload or []
    for i, item in enumerate(items):
        if isinstance(item, dict):
            segments.append(
                TranscriptSegment(
                    index=int(item.get("index", i)),
                    start=item.get("start"),
                    end=item.get("end"),
                    text=str(item.get("text", item.get("word", ""))),
                    speaker=item.get("speaker"),
                )
            )
    return segments


def normalize_transcript(result: Any) -> TranscriptResult:
    text = getattr(result, "text", None) or result.get("text", "") if isinstance(result, dict) else ""
    segments = []
    if isinstance(result, dict):
        segments = normalize_segments(result.get("segments") or result.get("words") or [])
    return TranscriptResult(text=text, segments=segments, raw=result)
