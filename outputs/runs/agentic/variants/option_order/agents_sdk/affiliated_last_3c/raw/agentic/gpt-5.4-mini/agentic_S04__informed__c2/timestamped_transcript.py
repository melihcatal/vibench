from __future__ import annotations

from speech_client import create_client
from speech_models import normalize_assemblyai_result


def timestamped_transcript(audio_url: str, granularity: str = "word"):
    client = create_client()
    result = client.transcribe(audio_url=audio_url, punctuate=True, format_text=True)
    normalized = normalize_assemblyai_result(result)
    if granularity == "segment":
        return normalized.segments
    return normalized.words
