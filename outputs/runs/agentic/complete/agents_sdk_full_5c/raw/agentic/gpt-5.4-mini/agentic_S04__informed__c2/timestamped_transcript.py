from __future__ import annotations

from typing import Any, Dict, List

from speech_client import get_transcriber
from speech_models import normalize_words


def timestamped_transcript(transcript_id: str, include_words: bool = True) -> Dict[str, Any]:
    transcriber = get_transcriber()
    transcript = transcriber.get_by_id(transcript_id)
    words = normalize_words(getattr(transcript, "words", []) or []) if include_words else []
    segments: List[Dict[str, Any]] = []
    for utterance in getattr(transcript, "utterances", []) or []:
        segments.append(
            {
                "speaker": getattr(utterance, "speaker", None),
                "start": getattr(utterance, "start", None),
                "end": getattr(utterance, "end", None),
                "text": getattr(utterance, "text", "") or "",
            }
        )
    return {
        "transcript_id": transcript.id,
        "status": transcript.status,
        "word_timestamps": words,
        "segment_timestamps": segments,
    }
