import os
from dataclasses import dataclass


@dataclass
class SpeechClientConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    transcription_model: str = "gpt-4o-transcribe"
    text_model: str = "gpt-4.1-mini"


def load_speech_config() -> SpeechClientConfig:
    api_key = os.getenv("OPENAI_API_KEY", "")
    return SpeechClientConfig(api_key=api_key)


def auth_headers() -> dict:
    cfg = load_speech_config()
    return {"Authorization": f"Bearer {cfg.api_key}"} if cfg.api_key else {}


def openai_base_url() -> str:
    return load_speech_config().base_url
