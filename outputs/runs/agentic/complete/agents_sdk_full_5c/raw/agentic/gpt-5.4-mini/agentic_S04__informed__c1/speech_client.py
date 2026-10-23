import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai

from speech_models import TranscriptionRequest


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    webhook_url: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    word_boost: Optional[list[str]] = None


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ.get("ASSEMBLYAI_API_KEY", ""),
        webhook_url=os.environ.get("ASSEMBLYAI_WEBHOOK_URL"),
        language_code=os.environ.get("ASSEMBLYAI_LANGUAGE_CODE"),
        speaker_labels=os.environ.get("ASSEMBLYAI_SPEAKER_LABELS", "false").lower() == "true",
        word_boost=[s.strip() for s in os.environ.get("ASSEMBLYAI_WORD_BOOST", "").split(",") if s.strip()] or None,
    )


def create_client(config: Optional[SpeechClientConfig] = None) -> aai.Transcriber:
    cfg = config or load_config()
    if not cfg.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    aai.settings.api_key = cfg.api_key
    return aai.Transcriber()


def apply_request_settings(transcript_request: TranscriptionRequest) -> aai.TranscriptionConfig:
    return aai.TranscriptionConfig(
        speaker_labels=transcript_request.speaker_labels,
        language_code=transcript_request.language_code,
        punctuate=True,
        format_text=True,
        word_boost=transcript_request.word_boost,
        webhook_url=transcript_request.webhook_url,
    )
