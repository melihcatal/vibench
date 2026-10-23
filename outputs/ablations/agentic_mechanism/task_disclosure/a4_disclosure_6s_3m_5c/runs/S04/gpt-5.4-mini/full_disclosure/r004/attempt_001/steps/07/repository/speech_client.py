import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    base_url: str = ASSEMBLYAI_BASE_URL
    timeout_seconds: int = 30


def load_speech_client_config(api_key: Optional[str] = None, base_url: Optional[str] = None, timeout_seconds: int = 30) -> SpeechClientConfig:
    token = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not token:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return SpeechClientConfig(api_key=token, base_url=base_url or ASSEMBLYAI_BASE_URL, timeout_seconds=timeout_seconds)


def build_speech_headers(config: SpeechClientConfig) -> Dict[str, str]:
    return {"authorization": config.api_key, "content-type": "application/json"}


def create_speech_session(config: Optional[SpeechClientConfig] = None) -> requests.Session:
    resolved = config or load_speech_client_config()
    session = requests.Session()
    session.headers.update(build_speech_headers(resolved))
    session.timeout = resolved.timeout_seconds  # type: ignore[attr-defined]
    return session


def speech_request(method: str, path: str, *, config: Optional[SpeechClientConfig] = None, **kwargs: Any) -> requests.Response:
    resolved = config or load_speech_client_config()
    url = f"{resolved.base_url.rstrip('/')} /{path.lstrip('/')}".replace(" ", "")
    response = requests.request(method, url, headers=build_speech_headers(resolved), timeout=kwargs.pop("timeout", resolved.timeout_seconds), **kwargs)
    response.raise_for_status()
    return response
