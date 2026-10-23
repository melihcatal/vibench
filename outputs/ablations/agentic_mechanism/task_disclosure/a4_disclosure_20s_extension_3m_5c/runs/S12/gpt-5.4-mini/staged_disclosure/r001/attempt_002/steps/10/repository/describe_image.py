import base64
import json
import os
import sys
from urllib import request


def describe_image(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "model": "gpt-5.4-mini",
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Write a short visual description of this image."},
                    {"type": "input_image", "image_url": f"data:image/*;base64,{image_b64}"},
                ],
            }
        ],
        "max_output_tokens": 60,
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

    text = data.get("output_text")
    if text:
        return text.strip()

    output = data.get("output", [])
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                return content["text"].strip()

    raise RuntimeError("No description returned")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python describe_image.py <image_path>")
    print(describe_image(sys.argv[1]))
