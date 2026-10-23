import base64
import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


OPENAI_VISION_MODEL = "gpt-4.1-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lstrip(".").lower() or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def detect_image_labels(image_path: str, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Identify the main visible objects and labels in this image. Return JSON with an array named labels. Each item should have name and confidence fields."},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
                ],
            }
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    labels = parsed.get("labels", [])
    if not isinstance(labels, list):
        raise ValueError("Invalid response format: labels must be a list")
    return labels


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: detect_image_labels.py IMAGE_PATH")
    labels = detect_image_labels(sys.argv[1])
    print(json.dumps({"labels": labels}, ensure_ascii=False))


if __name__ == "__main__":
    main()
