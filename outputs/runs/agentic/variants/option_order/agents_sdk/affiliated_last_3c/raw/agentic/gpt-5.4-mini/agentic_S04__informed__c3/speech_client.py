from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai

from speech_models import TranscriptResult


@dataclass
class SpeechClientConfig:
    api_key: str
    default_language: Optional[str] = None


def load_config() -> SpeechClientConfig:
    api_key = os.getenv("ASSEMBLYAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    default_language = os.getenv("ASSEMBLYAI_LANGUAGE_CODE")
    return SpeechClientConfig(api_key=api_key, default_language=default_language)


def create_client() -> aai.Transcriber:
    config = load_config()
    aai.settings.api_key = config.api_key
    return aai.Transcriber()


def normalize_transcript(transcript: object) -> TranscriptResult:
    if hasattr(transcript, "dict"):
        data = transcript.dict()
    elif isinstance(transcript, dict):
        data = transcript
    else:
        data = {"id": getattr(transcript, "id", ""), "status": getattr(transcript, "status", ""), "text": getattr(transcript, "text", "")}
    return TranscriptResult.from_assemblyai(data)
