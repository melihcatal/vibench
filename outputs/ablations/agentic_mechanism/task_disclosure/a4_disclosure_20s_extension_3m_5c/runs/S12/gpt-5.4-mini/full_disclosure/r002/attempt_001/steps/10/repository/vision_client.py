import os
from dataclasses import dataclass
from typing import Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_VISION_MODEL = "gpt-4o-mini"
OPENAI_SAFETY_MODEL = "omni-moderation-latest"


@dataclass(frozen=True)
class VisionConfig:
    api_key: str
    chat_completions_url: str = OPENAI_CHAT_COMPLETIONS_URL
    responses_url: str = OPENAI_RESPONSES_URL
    vision_model: str = OPENAI_VISION_MODEL
    safety_model: str = OPENAI_SAFETY_MODEL


def get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def get_config(api_key: Optional[str] = None) -> VisionConfig:
    return VisionConfig(api_key=get_api_key(api_key))


def build_headers(api_key: Optional[str] = None) -> dict:
    key = get_api_key(api_key)
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def create_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update(build_headers(api_key))
    return session


def normalize_image_mime_type(image_path: str) -> str:
    lower = image_path.lower()
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    if lower.endswith(".webp"):
        return "image/webp"
    if lower.endswith(".gif"):
        return "image/gif"
    return "image/jpeg"
