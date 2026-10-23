import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = "https://api.openai.com/v1/responses"


def _load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def _image_to_data_url(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def score_image_safety(image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    image_bytes = _load_image_bytes(image_path)
    data_url = _image_to_data_url(image_bytes)

    payload: Dict[str, Any] = {
        "model": OPENAI_VISION_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Assess this image for unsafe or policy-sensitive visual content. Return a concise JSON object with keys unsafe (boolean), severity (one of low, medium, high), categories (array of strings), and rationale (string).",
                    },
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
        "max_output_tokens": 200,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    return {"unsafe": False, "severity": "low", "categories": [], "rationale": text.strip()}


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python score_image_safety.py IMAGE_PATH")
    print(json.dumps(score_image_safety(sys.argv[1]), ensure_ascii=False))
