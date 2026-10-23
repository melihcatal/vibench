import base64
import os
from typing import Any, Dict

import requests

from vision_models import VisionImageRequest, VisionResult, normalize_labels, normalize_texts


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def _encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _chat_completion(prompt: str, image_path: str) -> Dict[str, Any]:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_encode_image(image_path)}"}},
                ],
            }
        ],
        "temperature": 0,
    }
    response = requests.post(url, headers=headers, json=body, timeout=60)
    response.raise_for_status()
    return response.json()


def run_vision_request(request: VisionImageRequest) -> VisionResult:
    raw = _chat_completion(request.prompt, request.image_path)
    content = raw["choices"][0]["message"]["content"]
    return VisionResult(
        provider="openai",
        content=content,
        raw=raw,
        labels=normalize_labels(raw.get("labels") or []),
        texts=normalize_texts(raw.get("texts") or []),
        safety=raw.get("safety"),
    )


def ensure_api_key() -> None:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
