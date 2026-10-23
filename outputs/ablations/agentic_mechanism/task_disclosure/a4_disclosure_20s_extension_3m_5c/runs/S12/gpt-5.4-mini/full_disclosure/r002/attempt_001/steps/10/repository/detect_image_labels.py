import base64
import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_VISION_MODEL = "gpt-4o-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _load_image_data(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def _build_prompt() -> str:
    return (
        "Identify the main objects, entities, and visible labels in this image. "
        "Return a concise JSON array of strings only. "
        "Use short label names and avoid sentences."
    )


def detect_image_labels(image_path: str, api_key: Optional[str] = None) -> List[str]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    image_b64 = _load_image_data(image_path)
    payload: Dict[str, Any] = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _build_prompt()},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                    },
                ],
            }
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    try:
        parsed = json.loads(content)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except Exception:
        pass
    return [line.strip("-• \t") for line in content.splitlines() if line.strip()]
