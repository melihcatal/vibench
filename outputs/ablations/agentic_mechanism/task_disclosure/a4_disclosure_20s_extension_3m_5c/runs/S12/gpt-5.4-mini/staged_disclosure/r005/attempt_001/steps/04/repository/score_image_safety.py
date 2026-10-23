import base64
import json
import os
import sys
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4o-mini"


def _image_to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    encoded = base64.b64encode(raw).decode("ascii")
    ext = os.path.splitext(path)[1].lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def score_image_safety(image_path: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    data_url = _image_to_data_url(image_path)
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Assess this image for unsafe or policy-sensitive visual content. Return JSON with keys: unsafe (boolean), score (number from 0 to 1), categories (array of strings), rationale (string)."},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    if not text:
        raise RuntimeError("No JSON response returned by OpenAI")

    return json.loads(text)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python score_image_safety.py <image_path>")
    result = score_image_safety(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
