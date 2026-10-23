import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def detect_image_text(image_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    instruction = prompt or "Extract all visible text from this image. Return only the text, preserving line breaks when helpful."
    payload = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{_encode_image(image_path)}"
                        },
                    },
                ],
            }
        ],
        "temperature": 0,
        "max_tokens": 512,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_VISION_MODEL, "text": text}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: detect_image_text.py IMAGE_PATH")
    print(detect_image_text(sys.argv[1])["text"])
