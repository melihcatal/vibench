import os
from dataclasses import dataclass
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class TranslationClientConfig:
    api_key: str
    model: str = OPENAI_MODEL
    timeout: int = 60


def get_translation_client_config(api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 60) -> TranslationClientConfig:
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return TranslationClientConfig(api_key=resolved_api_key, model=model or OPENAI_MODEL, timeout=timeout)


def build_translation_headers(api_key: str) -> dict:
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def create_translation_session(api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 60) -> requests.Session:
    config = get_translation_client_config(api_key=api_key, model=model, timeout=timeout)
    session = requests.Session()
    session.headers.update(build_translation_headers(config.api_key))
    session.headers.update({"X-Translation-Model": config.model})
    return session
