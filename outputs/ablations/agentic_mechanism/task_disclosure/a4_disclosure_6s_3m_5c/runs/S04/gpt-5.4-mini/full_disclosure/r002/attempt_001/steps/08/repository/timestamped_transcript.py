import os
from typing import Any, Dict, List, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


class TimestampedTranscriptError(RuntimeError):
    pass


def _api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise TimestampedTranscriptError("Missing ASSEMBLYAI_API_KEY")
    return key


def _headers(api_key: str) -> Dict[str, str]:
    return {"authorization": api_key}


def _get_json(url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def _normalize_words(words: Any) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not isinstance(words, list):
        return normalized
    for word in words:
        if isinstance(word, dict):
            normalized.append(
                {
                    "text": word.get("text"),
                    "start": word.get("start"),
                    "end": word.get("end"),
                    "confidence": word.get("confidence"),
                    "speaker": word.get("speaker"),
                }
            )
    return normalized


def _normalize_segments(segments: Any) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not isinstance(segments, list):
        return normalized
    for segment in segments:
        if isinstance(segment, dict):
            normalized.append(
                {
                    "text": segment.get("text"),
                    "start": segment.get("start"),
                    "end": segment.get("end"),
                    "speaker": segment.get("speaker"),
                    "words": _normalize_words(segment.get("words")),
                }
            )
    return normalized


def timestamped_transcript(
    transcription_id: str,
    api_key: Optional[str] = None,
    timestamps: str = "word",
) -> Dict[str, Any]:
    key = _api_key(api_key)
    if timestamps not in {"word", "segment"}:
        raise TimestampedTranscriptError("timestamps must be 'word' or 'segment'")

    result = _get_json(f"{ASSEMBLYAI_API_BASE}/transcript/{transcription_id}", _headers(key))
    if result.get("status") != "completed":
        raise TimestampedTranscriptError("Transcript is not completed")

    if timestamps == "word":
        return {"transcription_id": transcription_id, "word_timestamps": _normalize_words(result.get("words"))}

    return {"transcription_id": transcription_id, "segment_timestamps": _normalize_segments(result.get("segments"))}
