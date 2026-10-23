import base64
import json
import os
import urllib.request


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _load_image_bytes(image_path):
    with open(image_path, "rb") as f:
        return f.read()


def _image_to_data_url(image_bytes, mime_type):
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def describe_image(image_path, mime_type="image/jpeg"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    image_bytes = _load_image_bytes(image_path)
    payload = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Write a short visual description of this image in one sentence."},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_bytes, mime_type)}},
                ],
            }
        ],
        "max_tokens": 60,
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: describe_image.py IMAGE_PATH [MIME_TYPE]")
    path = sys.argv[1]
    mime = sys.argv[2] if len(sys.argv) > 2 else "image/jpeg"
    print(describe_image(path, mime))
