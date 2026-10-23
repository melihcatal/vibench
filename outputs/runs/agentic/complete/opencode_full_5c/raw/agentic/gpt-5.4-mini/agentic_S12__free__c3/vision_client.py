import base64
import os
from typing import Any, Dict

import requests

from vision_models import VisionRequest, VisionResult, normalize_labels, normalize_text


class VisionClient:
    def __init__(self, api_key: str | None = None, endpoint: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv(
            "OPENAI_API_BASE", "https://api.openai.com/v1"
        )

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def analyze(self, request: VisionRequest, purpose: str) -> VisionResult:
        payload: Dict[str, Any] = {
            "model": "openai/gpt-5.4-mini",
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": request.prompt or purpose},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{self._encode_image(request.image_path)}",
                        },
                    ],
                }
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{self.endpoint}/responses", json=payload, headers=headers, timeout=60
        )
        response.raise_for_status()
        data = response.json()
        output_text = normalize_text(data.get("output_text") or data)
        labels = normalize_labels(data.get("labels") or data.get("objects") or [])
        unsafe = bool(data.get("unsafe") or data.get("safety", {}).get("unsafe"))
        return VisionResult(text=output_text, labels=labels, unsafe=unsafe, raw=data)


def get_client() -> VisionClient:
    return VisionClient()
