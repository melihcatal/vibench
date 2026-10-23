from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from openai import OpenAI


MODEL = os.environ.get("OPENAI_TRANSCRIPTION_MODEL", "whisper-1")


def transcribe_sample(audio_path: str, language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with Path(audio_path).open("rb") as f:
        kwargs = {"model": MODEL, "file": f}
        if language:
            kwargs["language"] = language
        response = client.audio.transcriptions.create(**kwargs)
    return response.text
