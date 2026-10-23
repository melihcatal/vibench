from __future__ import annotations

import base64
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from vision_models import ImageAnalysisResult, VisualRequest

OPENAI_API_HOST = "https://api.openai.com/v1"
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")


def _load_bytes(image_path: str) -> bytes:
    return Path(image_path).expanduser().read_bytes()


def _data_url(image_path: str) -> str:
    ext = Path(image_path).suffix.lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    b64 = base64.b64encode(_load_bytes(image_path)).decode("ascii")
    return f"data:image/{mime};base64,{b64}"


class OpenAIVisionClient:
    def __init__(self, api_key: Optional[str] = None, model: str = OPENAI_VISION_MODEL):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model
        self.base_url = OPENAI_API_HOST
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def analyze_image(self, request: VisualRequest, instruction: str) -> ImageAnalysisResult:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction if not request.prompt else f"{instruction}\n{request.prompt}"},
                        {"type": "image_url", "image_url": {"url": _data_url(request.image_path)}},
                    ],
                }
            ],
            "temperature": 0.2,
        }
        resp = requests.post(f"{self.base_url}/chat/completions", headers=self._headers(), data=json.dumps(payload), timeout=60)
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        return ImageAnalysisResult(provider="openai", kind="analysis", text=text, raw=data)

    def safety_score(self, request: VisualRequest) -> ImageAnalysisResult:
        instruction = "Assess the image for explicit, violent, self-harm, hateful, or otherwise unsafe visual content. Respond with a brief risk summary and a score from 0 to 1."
        return self.analyze_image(request, instruction)


def load_request(image_path: str, prompt: Optional[str] = None, language: Optional[str] = None) -> VisualRequest:
    return VisualRequest(image_path=image_path, prompt=prompt, language=language)
