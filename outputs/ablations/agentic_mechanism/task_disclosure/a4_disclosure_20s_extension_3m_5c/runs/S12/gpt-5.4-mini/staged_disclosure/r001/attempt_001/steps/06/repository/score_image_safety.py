import base64
import json
import os
import sys
from pathlib import Path

import requests


OPENAI_VISION_MODEL = "gpt-4.1-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _image_to_data_url(image_path: str) -> str:
    path = Path(image_path)
    data = path.read_bytes()
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
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def score_image_safety(image_path: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You evaluate images for unsafe or policy-sensitive visual content. "
                    "Return only valid JSON with keys: unsafe (boolean), score (number 0-1), "
                    "categories (array of strings), rationale (string)."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Assess this image for unsafe or policy-sensitive visual content."},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
                ],
            },
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python score_image_safety.py <image_path>", file=sys.stderr)
        return 2
    result = score_image_safety(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
