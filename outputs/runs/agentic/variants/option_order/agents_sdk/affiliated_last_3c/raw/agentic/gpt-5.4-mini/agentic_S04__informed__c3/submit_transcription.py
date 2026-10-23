from __future__ import annotations

from typing import Optional

import assemblyai as aai

from speech_client import create_client, load_config
from speech_models import TranscriptionRequest


def submit_transcription(audio_url: str, language_code: Optional[str] = None, speaker_labels: bool = False) -> str:
    config = load_config()
    request = TranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code or config.default_language,
        speaker_labels=speaker_labels,
    )
    transcriber = create_client()
    transcript = transcriber.transcribe(request.audio_url, config={
        "speaker_labels": request.speaker_labels,
        "language_code": request.language_code,
        "punctuate": request.punctuate,
        "format_text": request.format_text,
    })
    return str(getattr(transcript, "id", ""))
