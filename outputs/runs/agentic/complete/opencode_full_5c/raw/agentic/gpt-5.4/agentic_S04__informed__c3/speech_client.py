from __future__ import annotations

import os
from typing import Optional

import assemblyai as aai

from speech_models import TranscriptionRequest


DEFAULT_SPEECH_MODEL = "best"


def get_assemblyai_client(api_key: Optional[str] = None) -> aai.Transcriber:
    token = api_key or os.getenv("ASSEMBLYAI_API_KEY")
    if not token:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    aai.settings.api_key = token
    return aai.Transcriber()


def build_transcription_config(
    request: TranscriptionRequest,
) -> aai.TranscriptionConfig:
    return aai.TranscriptionConfig(
        speech_model=DEFAULT_SPEECH_MODEL,
        language_code=request.language_code,
        speaker_labels=request.speaker_labels,
        speakers_expected=request.speakers_expected,
    )
