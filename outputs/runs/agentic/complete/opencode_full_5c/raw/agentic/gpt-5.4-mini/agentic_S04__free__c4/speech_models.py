from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    file_path: str
    language: Optional[str] = None
    prompt: Optional[str] = None
    temperature: Optional[float] = None


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    speaker: Optional[str] = None
    tokens: Optional[List[Dict[str, Any]]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return " ".join(normalize_text(item) for item in value if normalize_text(item))
    return str(value).strip()


def extract_segments(payload: Any) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    if payload is None:
        return segments
    if isinstance(payload, dict):
        items = payload.get("segments") or payload.get("words") or []
        for item in items:
            segments.append(
                TranscriptSegment(
                    text=normalize_text(item.get("text") or item.get("word") or ""),
                    start=item.get("start"),
                    end=item.get("end"),
                    speaker=item.get("speaker"),
                    tokens=item.get("tokens"),
                )
            )
    return segments
