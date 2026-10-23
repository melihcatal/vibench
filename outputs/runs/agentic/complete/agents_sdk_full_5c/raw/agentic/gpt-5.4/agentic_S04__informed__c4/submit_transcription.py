from __future__ import annotations

from speech_client import build_config, get_client, job_from_transcript
from speech_models import TranscriptJob


def submit_transcription(audio_url: str, language_code: str | None = None) -> TranscriptJob:
    transcriber = get_client()
    config = build_config(language_code=language_code)
    transcript = transcriber.submit(audio_url, config=config)
    return job_from_transcript(transcript, audio_url=audio_url)
