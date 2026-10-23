import base64
import json
import mimetypes
import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _load_image_as_data_url(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def describe_image(image_path: str, api_key: Optional[str] = None) -> str:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    image_url = _load_image_as_data_url(image_path)
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Write a short visual description of this image in one sentence.",
                    },
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        "temperature": 0,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate a short visual description for an image using OpenAI.")
    parser.add_argument("image_path")
    args = parser.parse_args()
    print(describe_image(args.image_path))


if __name__ == "__main__":
    main()
