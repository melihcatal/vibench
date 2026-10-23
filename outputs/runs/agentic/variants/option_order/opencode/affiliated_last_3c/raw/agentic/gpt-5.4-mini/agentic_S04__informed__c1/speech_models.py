from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SpeechJobRequest:
    audio_url: str
    language_code: Optional[str] = None
    diarization: bool = False
    word_timestamps: bool = False
    utterance_timestamps: bool = False


@dataclass
class SpeechJobResult:
    job_id: str
    status: str
    transcript: Optional[str] = None
    segments: Optional[List[Dict[str, Any]]] = None


def normalize_segments(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = payload.get("segments") or payload.get("utterances") or []
    normalized = []
    for item in segments:
        normalized.append(
            {
                "speaker": item.get("speaker")
                or item.get("speaker_label")
                or item.get("speaker_id"),
                "start": item.get("start"),
                "end": item.get("end"),
                "text": item.get("text") or item.get("transcript"),
                "words": item.get("words") or [],
            }
        )
    return normalized


def transcript_text(payload: Dict[str, Any]) -> str:
    if payload.get("text"):
        return payload["text"]
    segments = normalize_segments(payload)
    return " ".join(
        segment.get("text", "") for segment in segments if segment.get("text")
    )
