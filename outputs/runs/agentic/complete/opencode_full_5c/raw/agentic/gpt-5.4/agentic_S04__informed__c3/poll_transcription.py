from __future__ import annotations

from speech_client import get_assemblyai_client
from speech_models import TranscriptResult, normalize_assemblyai_transcript


def poll_transcription(transcript_id: str) -> TranscriptResult:
    client = get_assemblyai_client()
    transcript = client.get_by_id(transcript_id)
    return normalize_assemblyai_transcript(transcript)
