import base64
import json
import os
from typing import List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _encode_image_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext or "png"
    return f"data:image/{mime};base64,{encoded}"


def detect_image_text(image_path: str, max_lines: int = 20) -> List[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Read all visible text in the image. Return the text as a JSON array of strings, "
        f"with at most {max_lines} entries, preserving line order and with no extra text."
    )
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _encode_image_data_url(image_path)}},
                ],
            }
        ],
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
    content = data["choices"][0]["message"]["content"].strip()
    try:
        lines = json.loads(content)
    except json.JSONDecodeError:
        lines = [line.strip("- •\n\t ") for line in content.splitlines() if line.strip()]
    return [str(line) for line in lines][:max_lines]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("--max-lines", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(detect_image_text(args.image_path, args.max_lines)))
