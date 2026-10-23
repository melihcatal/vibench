import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    webhook_url: Optional[str] = None
    language_code: Optional[str] = None


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ.get("ASSEMBLYAI_API_KEY", ""),
        webhook_url=os.environ.get("ASSEMBLYAI_WEBHOOK_URL"),
        language_code=os.environ.get("ASSEMBLYAI_LANGUAGE_CODE"),
    )


def configure_client() -> aai.Transcriber:
    config = load_speech_config()
    if config.api_key:
        aai.settings.api_key = config.api_key
    return aai.Transcriber()


def audio_source_from_path(audio_path: str) -> aai.types.TranscriptInput:
    return audio_path
