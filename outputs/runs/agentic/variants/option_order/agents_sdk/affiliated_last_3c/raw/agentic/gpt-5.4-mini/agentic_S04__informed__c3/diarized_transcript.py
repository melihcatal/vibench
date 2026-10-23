from __future__ import annotations

from speech_client import create_client, normalize_transcript


def diarized_transcript(audio_url: str):
    client = create_client()
    transcript = client.transcribe(audio_url, config={"speaker_labels": True, "punctuate": True, "format_text": True})
    return normalize_transcript(transcript)
