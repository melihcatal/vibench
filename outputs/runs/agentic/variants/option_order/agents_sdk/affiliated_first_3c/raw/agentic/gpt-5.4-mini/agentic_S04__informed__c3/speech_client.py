import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    webhook_url: Optional[str] = None
    language_code: Optional[str] = None


def load_speech_config() -> SpeechConfig:
    api_key = os.getenv("ASSEMBLYAI_API_KEY", "")
    webhook_url = os.getenv("ASSEMBLYAI_WEBHOOK_URL")
    language_code = os.getenv("ASSEMBLYAI_LANGUAGE_CODE")
    return SpeechConfig(api_key=api_key, webhook_url=webhook_url, language_code=language_code)


def configure_client() -> aai.Transcriber:
    config = load_speech_config()
    if not config.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    aai.settings.api_key = config.api_key
    return aai.Transcriber()


def normalize_audio_source(audio_source: str) -> str:
    if audio_source.startswith("file://"):
        return audio_source[7:]
    return audio_source
