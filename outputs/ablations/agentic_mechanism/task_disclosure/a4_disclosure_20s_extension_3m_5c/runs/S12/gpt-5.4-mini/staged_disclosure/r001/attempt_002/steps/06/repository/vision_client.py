import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")


@dataclass(frozen=True)
class VisionConfig:
    api_key: str
    base_url: str
    model: str


def load_config() -> VisionConfig:
    api_key = OPENAI_API_KEY
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return VisionConfig(api_key=api_key, base_url=OPENAI_API_BASE_URL, model=OPENAI_VISION_MODEL)


def _image_to_data_url(image_path: str) -> str:
    data = Path(image_path).read_bytes()
    ext = Path(image_path).suffix.lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:image/{mime};base64,{encoded}"


class VisionClient:
    def __init__(self, config: Optional[VisionConfig] = None) -> None:
        self.config = config or load_config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def generate_static_image(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        payload = {"model": self.config.model, "prompt": prompt, "size": size}
        response = self.session.post(f"{self.config.base_url}/images/generations", data=json.dumps(payload), timeout=120)
        response.raise_for_status()
        return response.json()

    def analyze_image(self, image_path: str, prompt: str = "Describe this image.") -> Dict[str, Any]:
        image_url = _image_to_data_url(image_path)
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            "max_tokens": 300,
        }
        response = self.session.post(f"{self.config.base_url}/chat/completions", data=json.dumps(payload), timeout=120)
        response.raise_for_status()
        return response.json()
