import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_VISION_SAFETY_MODEL = "omni-moderation-latest"
OPENAI_API_URL = "https://api.openai.com/v1/responses"


def _load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def _to_data_url(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def score_image_safety(image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    image_bytes = _load_image_bytes(image_path)
    payload = {
        "model": OPENAI_VISION_SAFETY_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Analyze this image for unsafe or policy-sensitive visual content. Return structured safety findings."},
                    {"type": "input_image", "image_url": _to_data_url(image_bytes)},
                ],
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    data = response.json()

    return {
        "provider": "openai",
        "model": OPENAI_VISION_SAFETY_MODEL,
        "response": data,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python score_image_safety.py <image_path>")
    result = score_image_safety(sys.argv[1])
    print(json.dumps(result, indent=2, sort_keys=True))
