import os
from dataclasses import dataclass
from typing import Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    base_url: str = ASSEMBLYAI_API_BASE
    request_timeout_seconds: float = 120.0


def load_speech_client_config(api_key: Optional[str] = None) -> SpeechClientConfig:
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return SpeechClientConfig(api_key=key)


def build_speech_headers(config: SpeechClientConfig) -> dict:
    return {"authorization": config.api_key}


def create_speech_session(config: Optional[SpeechClientConfig] = None) -> requests.Session:
    cfg = config or load_speech_client_config()
    session = requests.Session()
    session.headers.update(build_speech_headers(cfg))
    session.headers["content-type"] = "application/json"
    session.base_url = cfg.base_url  # type: ignore[attr-defined]
    session.request_timeout_seconds = cfg.request_timeout_seconds  # type: ignore[attr-defined]
    return session


def speech_api_url(path: str, config: Optional[SpeechClientConfig] = None) -> str:
    cfg = config or load_speech_client_config()
    return f"{cfg.base_url.rstrip('/')}/{path.lstrip('/')}"


def speech_request_timeout(config: Optional[SpeechClientConfig] = None) -> float:
    cfg = config or load_speech_client_config()
    return cfg.request_timeout_seconds
