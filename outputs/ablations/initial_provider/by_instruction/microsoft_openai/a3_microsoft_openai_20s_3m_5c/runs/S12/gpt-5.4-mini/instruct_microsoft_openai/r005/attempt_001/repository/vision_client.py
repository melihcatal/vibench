import base64
import os
from typing import Any, Dict, Optional

import requests

from vision_models import VisionRequest, VisionResult


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _image_data_uri(image_path: str) -> str:
    with open(image_path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("ascii")
    suffix = os.path.splitext(image_path)[1].lstrip(".").lower() or "png"
    return f"data:image/{suffix};base64,{encoded}"


def _post_vision(prompt: str, image_path: str, temperature: float = 0.2) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {
        "model": OPENAI_VISION_MODEL,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _image_data_uri(image_path)}},
                ],
            }
        ],
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    content = body["choices"][0]["message"]["content"]
    if isinstance(content, str):
        import json

        return json.loads(content)
    return content


def analyze_image(request: VisionRequest, prompt: Optional[str] = None) -> VisionResult:
    result = _post_vision(prompt or request.prompt, request.image_path)
    return VisionResult.from_payload(result)
