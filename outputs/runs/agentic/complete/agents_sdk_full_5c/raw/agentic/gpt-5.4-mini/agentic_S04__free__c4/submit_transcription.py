from __future__ import annotations

from pathlib import Path
from typing import Optional

from speech_client import OPENAI_TRANSCRIBE_MODEL, SpeechClientFactory
from speech_models import TranscriptionRequest


def submit_transcription(audio_path: str, prompt: Optional[str] = None, language: Optional[str] = None) -> str:
    client = SpeechClientFactory.create()
    req = TranscriptionRequest(audio_path=audio_path, model=OPENAI_TRANSCRIBE_MODEL, prompt=prompt, language=language)
    with Path(req.audio_path).open("rb") as audio_file:
        job = client.audio.transcriptions.create(file=audio_file, **req.to_kwargs())
    return getattr(job, "id", None) or job["id"]
