from __future__ import annotations

from openai import OpenAI

from speech_client import OPENAI_TRANSCRIBE_MODEL, ensure_audio_file, get_client
from speech_models import TranscriptionJobRequest, extract_transcript_fields


def submit_transcription(audio_path: str, language: str | None = None, prompt: str | None = None) -> dict:
    client: OpenAI = get_client()
    request = TranscriptionJobRequest(audio_path=ensure_audio_file(audio_path), language=language, prompt=prompt)
    with open(request.audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=request.model or OPENAI_TRANSCRIBE_MODEL,
            file=audio_file,
            language=request.language,
            prompt=request.prompt,
            response_format=request.response_format,
            timestamp_granularities=request.timestamp_granularities,
        )
    result = extract_transcript_fields(transcript)
    return {"text": result.text, "segments": result.segments, "words": result.words, "raw": result.raw}
