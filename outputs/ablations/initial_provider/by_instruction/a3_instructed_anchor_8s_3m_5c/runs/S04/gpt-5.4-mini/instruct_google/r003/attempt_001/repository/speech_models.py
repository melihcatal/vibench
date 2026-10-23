from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_segments(value: Any) -> List[Dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for key in ("segments", "words", "items"):
            if isinstance(value.get(key), list):
                return [item for item in value[key] if isinstance(item, dict)]
    return []


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "transcript", "content"):
            raw = value.get(key)
            if isinstance(raw, str):
                return raw
        segments = normalize_segments(value)
        texts = [str(seg.get("text", "")).strip() for seg in segments if str(seg.get("text", "")).strip()]
        if texts:
            return " ".join(texts)
    return str(value)


@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: Optional[str] = None
    diarization: bool = False
    enable_timestamps: bool = False


@dataclass
class TranscriptionResult:
    job_name: str
    transcript: str
    segments: List[Dict[str, Any]]
    raw: Dict[str, Any]
