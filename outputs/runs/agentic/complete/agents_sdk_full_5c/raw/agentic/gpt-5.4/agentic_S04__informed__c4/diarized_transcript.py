from __future__ import annotations

from speech_client import build_config, get_client, result_from_transcript
from speech_models import TranscriptResult


def diarized_transcript(audio_url: str, language_code: str | None = None) -> TranscriptResult:
    transcriber = get_client()
    config = build_config(language_code=language_code, speaker_labels=True)
    transcript = transcriber.transcribe(audio_url, config=config)
    return result_from_transcript(transcript)
