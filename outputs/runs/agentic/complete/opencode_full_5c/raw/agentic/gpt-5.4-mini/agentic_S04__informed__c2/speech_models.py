from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    webhook_url: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True


@dataclass
class TranscriptionResult:
    id: str
    status: str
    text: str = ""
    segments: Optional[List[Dict[str, Any]]] = None
    words: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


def normalize_segments(payload: Any) -> List[Dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [segment for segment in payload if isinstance(segment, dict)]
    if isinstance(payload, dict):
        for key in ("segments", "utterances", "words"):
            value = payload.get(key)
            if isinstance(value, list):
                return [segment for segment in value if isinstance(segment, dict)]
    return []


def normalize_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload.strip()
    if isinstance(payload, dict):
        for key in ("text", "transcript", "content"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""
