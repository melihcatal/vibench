import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


@dataclass(frozen=True)
class SafetyConfig:
    api_key: Optional[str] = None
    model: str = OPENAI_MODERATION_MODEL
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "SafetyConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODERATION_MODEL", OPENAI_MODERATION_MODEL),
            timeout=float(os.getenv("OPENAI_MODERATION_TIMEOUT", "30")),
        )


def _resolve_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def build_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = _resolve_api_key(api_key)
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def build_moderation_payload(text: Any, model: Optional[str] = None) -> Dict[str, Any]:
    if isinstance(text, str):
        input_value = text
    elif isinstance(text, list):
        input_value = text
    else:
        raise TypeError("text must be a string or list of strings")

    return {"model": model or OPENAI_MODERATION_MODEL, "input": input_value}


def create_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update(build_headers(api_key))
    return session


def request_moderation(
    text: Any,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
) -> Dict[str, Any]:
    payload = build_moderation_payload(text, model=model)
    session = create_session(api_key)
    response = session.post(
        OPENAI_MODERATION_API_URL,
        json=payload,
        timeout=timeout if timeout is not None else 30,
    )
    response.raise_for_status()
    return response.json()


def get_default_config() -> SafetyConfig:
    return SafetyConfig.from_env()
