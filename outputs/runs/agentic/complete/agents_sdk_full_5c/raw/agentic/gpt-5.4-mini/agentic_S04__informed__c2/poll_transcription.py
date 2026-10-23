from __future__ import annotations

from typing import Any, Dict

from speech_client import get_transcriber
from speech_models import TranscriptionResult, normalize_segments, normalize_words


def poll_transcription(transcript_id: str) -> Dict[str, Any]:
    transcriber = get_transcriber()
    transcript = transcriber.get_by_id(transcript_id)
    result = TranscriptionResult(
        transcript_id=transcript.id,
        status=transcript.status,
        text=getattr(transcript, "text", "") or "",
        segments=normalize_segments(getattr(transcript, "utterances", []) or []),
        words=normalize_words(getattr(transcript, "words", []) or []),
    )
    return {
        "transcript_id": result.transcript_id,
        "status": result.status,
        "text": result.text,
        "segments": [segment.__dict__ for segment in result.segments],
        "words": result.words,
    }
