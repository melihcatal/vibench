from __future__ import annotations

import io
import os
from typing import Optional

import openai


def transcribe_tts_sample(audio: bytes, language: Optional[str] = None) -> str:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    file_obj = io.BytesIO(audio)
    file_obj.name = "sample.wav"
    transcript = client.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=file_obj, language=language)
    return transcript.text
