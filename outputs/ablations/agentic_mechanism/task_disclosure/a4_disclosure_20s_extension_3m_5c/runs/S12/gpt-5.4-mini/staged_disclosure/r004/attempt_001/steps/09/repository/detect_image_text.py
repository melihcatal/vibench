import os
import sys
import json
import base64
from pathlib import Path

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_VISION_MODEL = "gpt-4o-mini"


def _image_to_data_url(image_path: Path) -> str:
    suffix = image_path.suffix.lower().lstrip('.')
    mime = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "tiff": "image/tiff",
        "tif": "image/tiff",
    }.get(suffix, "application/octet-stream")
    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def detect_image_text(image_path: str) -> str:
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all visible text from this image. Return only the text, preserving line breaks where helpful."},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(path)}},
                ],
            }
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python detect_image_text.py <image_path>")
    print(detect_image_text(sys.argv[1]))


if __name__ == "__main__":
    main()
