import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def extract_text(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(image_path)

    mime = "image/png"
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif suffix == ".webp":
        mime = "image/webp"
    elif suffix == ".gif":
        mime = "image/gif"

    image_b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all readable plain text from this scanned document image. Return only the text."},
                    {"type": "input_image", "image_url": f"data:{mime};base64,{image_b64}"},
                ],
            }
        ],
    }

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    texts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    texts.append(text)

    return "\n".join(texts).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    args = parser.parse_args()
    sys.stdout.write(extract_text(args.image_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
