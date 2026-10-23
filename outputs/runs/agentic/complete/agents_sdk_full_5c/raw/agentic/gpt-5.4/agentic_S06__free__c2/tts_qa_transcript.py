from __future__ import annotations

import os
from pathlib import Path
from typing import BinaryIO, Union

from openai import OpenAI

from speech_models import TranscriptResult


OPENAI_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"


def transcribe_qa_sample(audio_source: Union[str, Path, BinaryIO], *, language: str | None = None) -> TranscriptResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if hasattr(audio_source, "read"):
        response = client.audio.transcriptions.create(
            model=OPENAI_TRANSCRIPTION_MODEL,
            file=audio_source,
            language=language,
        )
    else:
        with open(audio_source, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=OPENAI_TRANSCRIPTION_MODEL,
                file=audio_file,
                language=language,
            )

    return TranscriptResult(
        transcript=getattr(response, "text", ""),
        language=language,
        raw_response=response.model_dump() if hasattr(response, "model_dump") else response,
    )
