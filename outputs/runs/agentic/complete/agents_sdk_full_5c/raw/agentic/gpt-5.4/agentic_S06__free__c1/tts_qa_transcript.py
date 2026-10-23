from __future__ import annotations

from pathlib import Path
from typing import Union

from openai import OpenAI


OPENAI_TRANSCRIBE_MODEL = "gpt-4o-mini-transcribe"


def transcribe_qa_sample(audio_file: Union[str, Path], api_key: str) -> str:
    client = OpenAI(api_key=api_key)
    with open(audio_file, "rb") as handle:
        transcript = client.audio.transcriptions.create(
            model=OPENAI_TRANSCRIBE_MODEL,
            file=handle,
        )
    return transcript.text
