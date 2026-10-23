from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _value(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def normalize_segments(result: Any) -> List[Dict[str, Any]]:
    segments = _value(result, "results", []) or _value(result, "segments", []) or []
    normalized = []
    for segment in segments:
        normalized.append({
            "text": _value(segment, "text", ""),
            "start": _value(segment, "start_time", _value(segment, "start", None)),
            "end": _value(segment, "end_time", _value(segment, "end", None)),
            "speaker": _value(segment, "speaker", _value(segment, "channel", None)),
        })
    return normalized


def normalize_transcript_text(result: Any) -> str:
    text = _value(result, "transcript", None)
    if text:
        return text
    segments = normalize_segments(result)
    return " ".join(s.get("text", "") for s in segments if s.get("text"))


@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
    enable_diarization: bool = False
    enable_timestamps: bool = False


@dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class ArchiveSummaryRequest:
    transcript: str


@dataclass
class EmbeddingRequest:
    text: str
