import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import speech


@dataclass(frozen=True)
class SpeechConfig:
    project_id: Optional[str]
    language_code: str
    sample_rate_hertz: int
    enable_punctuation: bool
    location: str


@lru_cache(maxsize=1)
def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        language_code=os.getenv('SPEECH_LANGUAGE_CODE', 'en-US'),
        sample_rate_hertz=int(os.getenv('SPEECH_SAMPLE_RATE_HZ', '16000')),
        enable_punctuation=os.getenv('SPEECH_ENABLE_PUNCTUATION', 'true').lower() in {'1', 'true', 'yes', 'on'},
        location=os.getenv('GOOGLE_CLOUD_LOCATION', 'global'),
    )


@lru_cache(maxsize=1)
def get_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()

