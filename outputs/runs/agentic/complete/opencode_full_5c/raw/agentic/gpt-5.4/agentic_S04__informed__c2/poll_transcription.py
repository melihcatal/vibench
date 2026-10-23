from __future__ import annotations

from speech_client import AssemblyAISpeechClient
from speech_models import TranscriptResult, normalize_transcript_response


def poll_transcription(transcript_id: str) -> TranscriptResult:
    client = AssemblyAISpeechClient()
    response = client.get_transcript(transcript_id)
    return normalize_transcript_response(response)
