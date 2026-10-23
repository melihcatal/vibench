import argparse
import base64
import json
import os
from pathlib import Path

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _encode_image(image_path: Path) -> str:
    return base64.b64encode(image_path.read_bytes()).decode("ascii")


def detect_labels(image_path: str) -> dict:
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    image_b64 = _encode_image(path)
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Detect the main labels or objects in this image. Return JSON with a labels array of short strings and a confidence field per label if available."},
                    {"type": "image_url", "image_url": {"url": f"data:image/{path.suffix.lstrip('.').lower()};base64,{image_b64}"}},
                ],
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0,
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect labels or objects in a static image using OpenAI Vision.")
    parser.add_argument("image_path", help="Path to the input image")
    args = parser.parse_args()
    result = detect_labels(args.image_path)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
