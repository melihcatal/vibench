from __future__ import annotations

import os
from io import BytesIO

import assemblyai as aai


def transcribe_qa_sample(audio_bytes: bytes, audio_format: str = "mp3") -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    aai.settings.api_key = api_key
    source = BytesIO(audio_bytes)
    source.name = f"qa_sample.{audio_format}"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(source)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return transcript.text or ""
