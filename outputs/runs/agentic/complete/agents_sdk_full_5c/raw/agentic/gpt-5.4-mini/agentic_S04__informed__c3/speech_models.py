from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class TranscriptionRequest:
    audio_url: Optional[str] = None
    audio_path: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    word_timestamps: bool = False


@dataclass(frozen=True)
class TranscriptionResponse:
    job_id: str
    status: str
    transcript: Optional[str] = None
    segments: Optional[List[Dict[str, Any]]] = None


def normalize_transcript_text(transcript: Any) -> str:
    if transcript is None:
        return ""
    if isinstance(transcript, str):
        return transcript.strip()
    return str(transcript).strip()


def normalize_segments(transcript_obj: Any) -> List[Dict[str, Any]]:
    utterances = getattr(transcript_obj, "utterances", None) or []
    words = getattr(transcript_obj, "words", None) or []
    segments: List[Dict[str, Any]] = []
    for item in utterances:
        segments.append(
            {
                "speaker": getattr(item, "speaker", None),
                "start": getattr(item, "start", None),
                "end": getattr(item, "end", None),
                "text": getattr(item, "text", None),
            }
        )
    if not segments and words:
        segments.append(
            {
                "speaker": None,
                "start": getattr(words[0], "start", None),
                "end": getattr(words[-1], "end", None),
                "text": " ".join(getattr(word, "text", "") for word in words).strip(),
                "words": [
                    {"text": getattr(word, "text", None), "start": getattr(word, "start", None), "end": getattr(word, "end", None)}
                    for word in words
                ],
            }
        )
    return segments
