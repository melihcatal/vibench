from __future__ import annotations

from typing import List

from speech_client import get_client
from speech_models import TranscriptSegment, normalize_sentences, normalize_words


def timestamped_transcript(transcript_id: str, level: str = "word") -> List[TranscriptSegment]:
    transcriber = get_client()
    transcript = transcriber.get_by_id(transcript_id)
    raw = getattr(transcript, "json_response", {}) or {}
    if level == "segment":
        return normalize_sentences(raw.get("sentences"))
    return normalize_words(raw.get("words"))
