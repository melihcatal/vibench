import os
from dataclasses import dataclass
from typing import Optional

import requests
from openai import OpenAI


OPENAI_TRANSCRIPTION_BASE_URL = "https://api.openai.com/v1"
OPENAI_TRANSCRIPTION_MODEL = "gpt-4o-transcribe"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    model: str = OPENAI_TRANSCRIPTION_MODEL
    base_url: str = OPENAI_TRANSCRIPTION_BASE_URL
    timeout: int = 120


def get_speech_client_config(api_key: Optional[str] = None, model: str = OPENAI_TRANSCRIPTION_MODEL, timeout: int = 120) -> SpeechClientConfig:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return SpeechClientConfig(api_key=key, model=model, timeout=timeout)


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    config = get_speech_client_config(api_key=api_key)
    return OpenAI(api_key=config.api_key)


def create_http_session(api_key: Optional[str] = None) -> requests.Session:
    config = get_speech_client_config(api_key=api_key)
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {config.api_key}"})
    return session
