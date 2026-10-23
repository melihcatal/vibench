import os
from typing import Any, Dict, List, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    return {"authorization": api_key, "content-type": "application/json"}


def _extract_words(transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
    words = transcript.get("words")
    if isinstance(words, list) and words:
        return words
    utterances = transcript.get("utterances")
    if isinstance(utterances, list):
        extracted: List[Dict[str, Any]] = []
        for utterance in utterances:
            if isinstance(utterance, dict):
                for word in utterance.get("words", []) or []:
                    if isinstance(word, dict):
                        extracted.append(word)
        if extracted:
            return extracted
    return []


def _extract_segments(transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
    utterances = transcript.get("utterances")
    if isinstance(utterances, list) and utterances:
        return [u for u in utterances if isinstance(u, dict)]
    paragraphs = transcript.get("paragraphs")
    if isinstance(paragraphs, dict):
        items = paragraphs.get("paragraphs")
        if isinstance(items, list):
            return [p for p in items if isinstance(p, dict)]
    return []


def get_timestamped_transcript(transcript: Dict[str, Any], mode: str = "word") -> List[Dict[str, Any]]:
    if mode == "word":
        return [
            {"text": word.get("text"), "start": word.get("start"), "end": word.get("end")}
            for word in _extract_words(transcript)
            if word.get("text") is not None
        ]
    if mode == "segment":
        return [
            {
                "text": segment.get("text"),
                "start": segment.get("start"),
                "end": segment.get("end"),
                "speaker": segment.get("speaker"),
            }
            for segment in _extract_segments(transcript)
            if segment.get("text") is not None
        ]
    raise ValueError('mode must be "word" or "segment"')


def fetch_timestamped_transcript(transcript_id: str, mode: str = "word") -> List[Dict[str, Any]]:
    response = requests.get(f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}", headers=_headers(), timeout=30)
    response.raise_for_status()
    transcript = response.json()
    status = transcript.get("status")
    if status == "error":
        raise RuntimeError(transcript.get("error", "transcription failed"))
    if status != "completed":
        raise ValueError(f"transcript is not completed: {status}")
    return get_timestamped_transcript(transcript, mode=mode)
