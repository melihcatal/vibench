from __future__ import annotations

from openai import OpenAI

from speech_client import get_client
from speech_models import extract_transcript_fields


def timestamped_transcript(audio_path: str, granularity: str = "word") -> dict:
    client: OpenAI = get_client()
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=[granularity],
        )
    result = extract_transcript_fields(transcript)
    return {"text": result.text, "segments": result.segments, "words": result.words, "raw": result.raw}
