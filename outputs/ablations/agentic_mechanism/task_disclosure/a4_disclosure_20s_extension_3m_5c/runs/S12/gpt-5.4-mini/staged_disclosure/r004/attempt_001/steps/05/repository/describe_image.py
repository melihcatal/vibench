import base64
import json
import os
import sys
from urllib import request


def _read_image_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def describe_image(image_path):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    image_bytes = _read_image_bytes(image_path)
    data_url = "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Write a short visual description of this image in one sentence."},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
    }

    req = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text_parts = []
    for item in result.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                text_parts.append(content["text"])
    return "\n".join(text_parts).strip()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: describe_image.py IMAGE_PATH")
    print(describe_image(sys.argv[1]))


if __name__ == "__main__":
    main()
