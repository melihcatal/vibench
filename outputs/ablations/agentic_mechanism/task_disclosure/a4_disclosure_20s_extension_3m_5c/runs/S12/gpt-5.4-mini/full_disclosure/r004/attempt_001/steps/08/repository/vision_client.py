import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_VISION_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_VISION_MODEL = "gpt-4.1-mini"


@dataclass(frozen=True)
class VisionConfig:
    api_key: str
    model: str = OPENAI_VISION_MODEL
    endpoint: str = OPENAI_VISION_ENDPOINT
    timeout: float = 60.0


def load_vision_config() -> VisionConfig:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    model = os.environ.get("OPENAI_VISION_MODEL", OPENAI_VISION_MODEL)
    endpoint = os.environ.get("OPENAI_VISION_ENDPOINT", OPENAI_VISION_ENDPOINT)
    timeout = float(os.environ.get("OPENAI_VISION_TIMEOUT", "60"))
    return VisionConfig(api_key=api_key, model=model, endpoint=endpoint, timeout=timeout)


def image_path_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext or "png"
    return f"data:image/{mime};base64,{encoded}"


def create_openai_vision_payload(prompt: str, image_url: str, model: Optional[str] = None, temperature: float = 0) -> Dict[str, Any]:
    return {
        "model": model or OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        "temperature": temperature,
    }


def post_openai_vision(prompt: str, image_path: str, config: Optional[VisionConfig] = None, temperature: float = 0) -> Dict[str, Any]:
    cfg = config or load_vision_config()
    payload = create_openai_vision_payload(prompt, image_path_to_data_url(image_path), model=cfg.model, temperature=temperature)
    response = requests.post(
        cfg.endpoint,
        headers={"Authorization": f"Bearer {cfg.api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=cfg.timeout,
    )
    response.raise_for_status()
    return response.json()
