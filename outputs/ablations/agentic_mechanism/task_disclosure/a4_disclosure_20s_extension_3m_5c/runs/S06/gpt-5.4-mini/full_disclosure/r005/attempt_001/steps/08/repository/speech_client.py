import os
from dataclasses import dataclass
from typing import Optional

import requests


OPENAI_TTS_API_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_VOICE_CATALOG_URL = "https://api.openai.com/v1/audio/voices"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    model: str = OPENAI_TTS_MODEL
    timeout: int = 120


def get_api_key(api_key: Optional[str] = None) -> str:
    key = (api_key or os.getenv("OPENAI_API_KEY") or "").strip()
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def get_config(api_key: Optional[str] = None, model: str = OPENAI_TTS_MODEL, timeout: int = 120) -> SpeechClientConfig:
    return SpeechClientConfig(api_key=get_api_key(api_key), model=model, timeout=timeout)


def auth_headers(api_key: Optional[str] = None) -> dict:
    return {"Authorization": f"Bearer {get_api_key(api_key)}"}


def json_headers(api_key: Optional[str] = None) -> dict:
    headers = auth_headers(api_key)
    headers["Content-Type"] = "application/json"
    return headers


def session(api_key: Optional[str] = None) -> requests.Session:
    s = requests.Session()
    s.headers.update(auth_headers(api_key))
    return s


def post_speech(payload: dict, api_key: Optional[str] = None, timeout: Optional[int] = None) -> requests.Response:
    config = get_config(api_key=api_key)
    effective_timeout = timeout if timeout is not None else config.timeout
    return requests.post(OPENAI_TTS_API_URL, json=payload, headers=json_headers(config.api_key), timeout=effective_timeout)


def get_voice_catalog(api_key: Optional[str] = None, timeout: int = 30) -> requests.Response:
    return requests.get(OPENAI_TTS_VOICE_CATALOG_URL, headers=auth_headers(api_key), timeout=timeout)
