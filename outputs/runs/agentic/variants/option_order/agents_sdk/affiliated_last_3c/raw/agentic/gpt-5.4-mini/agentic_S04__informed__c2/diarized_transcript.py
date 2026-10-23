from __future__ import annotations

from speech_client import create_client
from speech_models import TranscriptRequest, normalize_assemblyai_result


def diarized_transcript(audio_url: str):
    client = create_client()
    req = TranscriptRequest(audio_url=audio_url, speaker_labels=True)
    result = client.transcribe(audio_url=req.audio_url, speaker_labels=req.speaker_labels)
    return normalize_assemblyai_result(result)
