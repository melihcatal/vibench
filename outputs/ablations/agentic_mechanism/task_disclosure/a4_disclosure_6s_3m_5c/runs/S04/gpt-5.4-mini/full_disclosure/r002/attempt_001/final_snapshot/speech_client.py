import os
from dataclasses import dataclass
from typing import Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


class SpeechClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    api_base: str = ASSEMBLYAI_API_BASE
    timeout: float = 30.0


def get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise SpeechClientError("Missing ASSEMBLYAI_API_KEY")
    return key


def get_config(api_key: Optional[str] = None, timeout: float = 30.0, api_base: str = ASSEMBLYAI_API_BASE) -> SpeechClientConfig:
    return SpeechClientConfig(api_key=get_api_key(api_key), api_base=api_base, timeout=timeout)


def get_headers(api_key: Optional[str] = None, content_type: Optional[str] = None) -> dict:
    headers = {"authorization": get_api_key(api_key)}
    if content_type is not None:
        headers["content-type"] = content_type
    return headers


def create_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update(get_headers(api_key))
    return session
