import base64
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")


@dataclass
class VisionConfig:
    api_key: str
    model: str = OPENAI_VISION_MODEL
    api_url: str = OPENAI_API_URL
    timeout: int = 60


def load_config() -> VisionConfig:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return VisionConfig(
        api_key=api_key,
        model=os.getenv("OPENAI_VISION_MODEL", OPENAI_VISION_MODEL),
        api_url=os.getenv("OPENAI_API_URL", OPENAI_API_URL),
        timeout=int(os.getenv("OPENAI_TIMEOUT", "60")),
    )


def image_to_data_url(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/png"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def build_vision_payload(prompt: str, image_path: str, model: Optional[str] = None) -> Dict[str, Any]:
    return {
        "model": model or OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
                ],
            }
        ],
        "temperature": 0,
    }


def post_vision_request(prompt: str, image_path: str, config: Optional[VisionConfig] = None, model: Optional[str] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    payload = build_vision_payload(prompt, image_path, model=model or cfg.model)
    response = requests.post(
        cfg.api_url,
        headers={
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=cfg.timeout,
    )
    response.raise_for_status()
    return response.json()
