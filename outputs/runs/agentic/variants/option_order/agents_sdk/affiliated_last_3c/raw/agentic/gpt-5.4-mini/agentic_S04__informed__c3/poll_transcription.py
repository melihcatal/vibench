from __future__ import annotations

from speech_client import create_client, normalize_transcript


def poll_transcription(transcription_id: str):
    client = create_client()
    transcript = client.get_transcript(transcription_id)
    return normalize_transcript(transcript)
