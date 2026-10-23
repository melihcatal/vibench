from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _segments(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("segments", "results", "words", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def normalize_transcript(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {"text": "", "status": None, "segments": []}
    if isinstance(payload, str):
        return {"text": payload, "status": None, "segments": []}
    if hasattr(payload, "to_dict"):
        payload = payload.to_dict()
    if hasattr(payload, "dict"):
        payload = payload.dict()
    if not isinstance(payload, dict):
        return {"text": str(payload), "status": None, "segments": []}
    text = (
        payload.get("text") or payload.get("transcript") or payload.get("content") or ""
    )
    status = payload.get("status") or payload.get("state")
    return {
        "text": text,
        "status": status,
        "segments": _segments(payload),
        "raw": payload,
    }


def transcript_text(payload: Any) -> str:
    return normalize_transcript(payload)["text"]


def transcript_segments(payload: Any) -> List[Dict[str, Any]]:
    return normalize_transcript(payload)["segments"]


@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_labels: bool = False
    word_timestamps: bool = False


@dataclass
class TranslationRequest:
    text: str
    target_language: str
