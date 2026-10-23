from __future__ import annotations

import os
from pathlib import Path

from openai import OpenAI

from speech_models import TranscriptResult


def transcribe_qa_sample(
    audio_file: str | Path, language: str | None = None
) -> TranscriptResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    file_path = Path(audio_file)
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    client = OpenAI(api_key=api_key)
    with file_path.open("rb") as handle:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe", file=handle, language=language
        )
    return TranscriptResult(text=transcript.text, language=language)
