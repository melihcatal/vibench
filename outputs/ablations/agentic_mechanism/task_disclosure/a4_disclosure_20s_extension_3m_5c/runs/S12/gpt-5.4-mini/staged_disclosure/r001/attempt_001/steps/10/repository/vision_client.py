import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_VISION_MODEL = "gpt-4.1-mini"


def _image_bytes(image_path: str | Path) -> bytes:
    return Path(image_path).read_bytes()


def _image_data_url(image_path: str | Path) -> str:
    path = Path(image_path)
    ext = path.suffix.lower().lstrip(".")
    mime = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "bmp": "image/bmp",
        "tif": "image/tiff",
        "tiff": "image/tiff",
    }.get(ext, "application/octet-stream")
    encoded = base64.b64encode(_image_bytes(path)).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


@dataclass(frozen=True)
class VisionClientConfig:
    api_key: str
    model: str = OPENAI_VISION_MODEL
    timeout: int = 60

    @classmethod
    def from_env(cls) -> "VisionClientConfig":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        model = os.environ.get("OPENAI_VISION_MODEL", OPENAI_VISION_MODEL)
        timeout = int(os.environ.get("OPENAI_VISION_TIMEOUT", "60"))
        return cls(api_key=api_key, model=model, timeout=timeout)


class VisionClient:
    def __init__(self, config: VisionClientConfig | None = None):
        self.config = config or VisionClientConfig.from_env()

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            OPENAI_API_URL,
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()

    def describe_image(self, image_path: str | Path) -> str:
        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Write a short visual description of this image."},
                        {"type": "input_image", "image_url": _image_data_url(image_path)},
                    ],
                }
            ],
        }
        data = self._post(payload)
        parts: list[str] = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    text = content.get("text", "")
                    if text:
                        parts.append(text)
        return "\n".join(parts).strip()

    def extract_text(self, image_path: str | Path) -> str:
        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Extract all visible text from this image. Return only the text."},
                        {"type": "input_image", "image_url": _image_data_url(image_path)},
                    ],
                }
            ],
        }
        data = self._post(payload)
        parts: list[str] = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    text = content.get("text", "")
                    if text:
                        parts.append(text)
        return "\n".join(parts).strip()

    def score_safety(self, image_path: str | Path) -> dict[str, Any]:
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You evaluate images for unsafe or policy-sensitive visual content. Return only valid JSON with keys: unsafe (boolean), score (number 0-1), categories (array of strings), rationale (string).",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Assess this image for unsafe or policy-sensitive visual content."},
                        {"type": "image_url", "image_url": {"url": _image_data_url(image_path)}},
                    ],
                },
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        data = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.config.timeout,
        )
        data.raise_for_status()
        return json.loads(data.json()["choices"][0]["message"]["content"])
