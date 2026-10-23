from __future__ import annotations

from speech_client import create_client
from speech_models import TranscriptRequest, normalize_assemblyai_result


def submit_transcription(audio_url: str):
    client = create_client()
    req = TranscriptRequest(audio_url=audio_url)
    result = client.transcribe(audio_url=req.audio_url)
    return normalize_assemblyai_result(result)
