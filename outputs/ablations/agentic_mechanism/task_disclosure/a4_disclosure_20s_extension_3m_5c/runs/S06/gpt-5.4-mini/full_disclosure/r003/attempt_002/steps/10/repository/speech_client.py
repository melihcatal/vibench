import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    base_url: str = OPENAI_API_BASE
    model: str = OPENAI_TTS_MODEL
    timeout: float = 120.0


def load_speech_config(api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None, timeout: Optional[float] = None) -> SpeechConfig:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return SpeechConfig(api_key=key, base_url=base_url or OPENAI_API_BASE, model=model or OPENAI_TTS_MODEL, timeout=timeout if timeout is not None else 120.0)


def build_auth_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def create_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update(build_auth_headers(api_key=api_key))
    return session


def speech_api_url(path: str, base_url: Optional[str] = None) -> str:
    root = (base_url or OPENAI_API_BASE).rstrip("/")
    suffix = path if path.startswith("/") else f"/{path}"
    return f"{root}{suffix}"


def request_json(method: str, path: str, *, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None, **kwargs: Any) -> Dict[str, Any]:
    config = load_speech_config(api_key=api_key, base_url=base_url, timeout=timeout)
    response = requests.request(method, speech_api_url(path, config.base_url), headers=build_auth_headers(config.api_key), timeout=config.timeout, **kwargs)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError("Unexpected response format")
    return payload


__all__ = ["OPENAI_API_BASE", "OPENAI_TTS_MODEL", "SpeechConfig", "load_speech_config", "build_auth_headers", "create_session", "speech_api_url", "request_json"]
