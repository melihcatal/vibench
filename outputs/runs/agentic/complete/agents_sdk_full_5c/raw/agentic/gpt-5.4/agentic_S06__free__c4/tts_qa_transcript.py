from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from speech_models import TranscriptResult


OPENAI_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"


def transcribe_qa_sample(audio_path: str, language: str | None = None) -> TranscriptResult:
    client = OpenAI()
    with Path(audio_path).open("rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=OPENAI_TRANSCRIPTION_MODEL,
            file=audio_file,
            language=language,
        )
    return TranscriptResult(
        text=response.text,
        language=language,
    )
