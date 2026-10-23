from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    audio_source: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    word_boost: Optional[List[str]] = None


@dataclass
class TranscriptionResult:
    id: str
    status: str
    text: str = ""
    transcript: str = ""
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None


def extract_text(result: Any) -> str:
    text = getattr(result, "text", None) or getattr(result, "transcript", None) or ""
    return str(text)


def normalize_result(result: Any) -> TranscriptionResult:
    return TranscriptionResult(
        id=str(getattr(result, "id", "")),
        status=str(getattr(result, "status", "")),
        text=extract_text(result),
        transcript=extract_text(result),
        words=getattr(result, "words", None),
        utterances=getattr(result, "utterances", None),
    )
