import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    base_url: str = "https://api.openai.com"
    timeout_seconds: float = 60.0
    organization: Optional[str] = None
    project: Optional[str] = None


def get_client_config() -> SpeechClientConfig:
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_SPEECH_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    return SpeechClientConfig(api_key=api_key, base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com"), timeout_seconds=float(os.environ.get("OPENAI_TIMEOUT_SECONDS", "60")), organization=os.environ.get("OPENAI_ORG_ID"), project=os.environ.get("OPENAI_PROJECT_ID"))


def build_url(config: SpeechClientConfig, path: str) -> str:
    return urljoin(config.base_url.rstrip("/") + "/", path.lstrip("/"))


def build_headers(config: SpeechClientConfig, multipart: bool = False) -> Dict[str, str]:
    headers = {"Authorization": f"Bearer {config.api_key}"}
    if multipart:
        headers["Accept"] = "application/json"
    else:
        headers["Content-Type"] = "application/json"
    if config.organization:
        headers["OpenAI-Organization"] = config.organization
    if config.project:
        headers["OpenAI-Project"] = config.project
    return headers


def ensure_file_path(path: str) -> str:
    if not path or not os.path.exists(path):
        raise FileNotFoundError(path)
    return path


def raise_for_api_error(response: requests.Response) -> None:
    try:
        payload: Any = response.json()
    except Exception:
        payload = response.text
    raise RuntimeError(f"OpenAI API error {response.status_code}: {payload}")
