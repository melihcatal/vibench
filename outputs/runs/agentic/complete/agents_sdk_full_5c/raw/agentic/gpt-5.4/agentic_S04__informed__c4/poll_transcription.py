from __future__ import annotations

from speech_client import get_client, result_from_transcript
from speech_models import TranscriptResult


def poll_transcription(transcript_id: str) -> TranscriptResult:
    transcriber = get_client()
    transcript = transcriber.get_by_id(transcript_id)
    return result_from_transcript(transcript)
