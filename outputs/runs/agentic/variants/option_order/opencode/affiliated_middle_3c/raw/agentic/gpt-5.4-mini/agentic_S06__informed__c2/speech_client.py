import os
from dataclasses import dataclass

import requests


@dataclass
class SpeechClientConfig:
    api_key: str
    base_url: str
    voice: str | None = None
    locale: str | None = None


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.environ.get("ELEVENLABS_API_KEY", ""),
        base_url=os.environ.get(
            "ELEVENLABS_API_BASE_URL", "https://api.elevenlabs.io/v1"
        ),
        voice=os.environ.get("ELEVENLABS_VOICE_ID"),
        locale=os.environ.get("ELEVENLABS_LOCALE"),
    )


def build_headers(api_key: str) -> dict:
    return {
        "xi-api-key": api_key,
        "content-type": "application/json",
        "accept": "audio/mpeg",
    }


def client_session() -> requests.Session:
    return requests.Session()
