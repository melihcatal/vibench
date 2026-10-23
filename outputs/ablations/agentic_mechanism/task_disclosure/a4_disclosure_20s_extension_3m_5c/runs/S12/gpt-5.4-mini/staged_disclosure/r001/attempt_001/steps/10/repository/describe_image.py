import base64
import json
import os
import sys
from urllib import request


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()


def describe_image(image_path):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    image_bytes = _read_image(image_path)
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Write a short visual description of this image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                ],
            }
        ],
        "max_tokens": 60,
    }

    req = request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return data["choices"][0]["message"]["content"].strip()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: describe_image.py <image_path>")
    print(describe_image(sys.argv[1]))


if __name__ == "__main__":
    main()
