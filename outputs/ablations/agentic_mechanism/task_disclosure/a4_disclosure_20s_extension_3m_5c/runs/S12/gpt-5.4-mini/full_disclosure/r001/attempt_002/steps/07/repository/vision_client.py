import os
from dataclasses import dataclass
from typing import Optional

import requests


OPENAI_DEFAULT_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
OPENAI_RESPONSES_API_URL = os.getenv("OPENAI_RESPONSES_API_URL", "https://api.openai.com/v1/responses")


@dataclass(frozen=True)
class VisionConfig:
    api_key: str
    model: str = OPENAI_DEFAULT_VISION_MODEL
    api_url: str = OPENAI_RESPONSES_API_URL
    timeout: int = 60


def get_openai_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def load_vision_config(api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 60) -> VisionConfig:
    return VisionConfig(
        api_key=get_openai_api_key(api_key),
        model=model or OPENAI_DEFAULT_VISION_MODEL,
        api_url=OPENAI_RESPONSES_API_URL,
        timeout=timeout,
    )


def create_vision_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {get_openai_api_key(api_key)}",
            "Content-Type": "application/json",
        }
    )
    return session


def vision_request_kwargs(config: VisionConfig) -> dict:
    return {"headers": {"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"}, "timeout": config.timeout}
