import base64
import json
import os
import sys
from urllib import request


def detect_image_text(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("ascii")
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all visible text from this image. Return only the text."},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{image_b64}"},
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
    with request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text"):
                parts.append(content.get("text", ""))
    return "".join(parts).strip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: detect_image_text.py IMAGE_PATH")
    print(detect_image_text(sys.argv[1]))
