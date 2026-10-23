import os
from dataclasses import dataclass
from typing import Optional

import requests


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class VisionConfig:
    google_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    timeout: int = 60


def load_vision_config() -> VisionConfig:
    return VisionConfig(
        google_api_key=os.environ.get("GOOGLE_CLOUD_VISION_API_KEY") or os.environ.get("GOOGLE_API_KEY"),
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        timeout=int(os.environ.get("VISION_API_TIMEOUT", "60")),
    )


def require_google_vision_key(config: Optional[VisionConfig] = None) -> str:
    config = config or load_vision_config()
    if not config.google_api_key:
        raise RuntimeError("Missing GOOGLE_CLOUD_VISION_API_KEY or GOOGLE_API_KEY")
    return config.google_api_key


def require_openai_key(config: Optional[VisionConfig] = None) -> str:
    config = config or load_vision_config()
    if not config.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return config.openai_api_key


def google_vision_session(config: Optional[VisionConfig] = None) -> requests.Session:
    config = config or load_vision_config()
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.params.update({"key": require_google_vision_key(config)})
    return session


def openai_session(config: Optional[VisionConfig] = None) -> requests.Session:
    config = config or load_vision_config()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {require_openai_key(config)}",
        "Content-Type": "application/json",
    })
    return session
