import base64
import json
import os
import sys
from urllib import request


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def extract_text_from_image(image_path: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all plain text from this scanned document image. Return only the text."},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{image_b64}"},
                ],
            }
        ],
        "temperature": 0,
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

    with request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    texts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                texts.append(content.get("text", ""))
    return "".join(texts).strip()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: extract_text.py <image_path>")
    print(extract_text_from_image(sys.argv[1]))


if __name__ == "__main__":
    main()
