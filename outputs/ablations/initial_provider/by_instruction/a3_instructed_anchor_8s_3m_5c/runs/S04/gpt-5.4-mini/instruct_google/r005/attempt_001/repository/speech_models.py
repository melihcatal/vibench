from dataclasses import dataclass
from typing import Any


@dataclass
class TranscriptResult:
    text: str
    segments: list[dict[str, Any]]
    words: list[dict[str, Any]]


def normalize_segments(segments: list[Any]) -> list[dict[str, Any]]:
    normalized = []
    for segment in segments:
        normalized.append({
            "start": getattr(segment, "start_time", None),
            "end": getattr(segment, "end_time", None),
            "text": getattr(segment, "transcript", None),
        })
    return normalized


def normalize_words(words: list[Any]) -> list[dict[str, Any]]:
    normalized = []
    for word in words:
        normalized.append({
            "word": getattr(word, "word", None),
            "start": getattr(word, "start_time", None),
            "end": getattr(word, "end_time", None),
            "speaker": getattr(word, "speaker_label", None),
        })
    return normalized
