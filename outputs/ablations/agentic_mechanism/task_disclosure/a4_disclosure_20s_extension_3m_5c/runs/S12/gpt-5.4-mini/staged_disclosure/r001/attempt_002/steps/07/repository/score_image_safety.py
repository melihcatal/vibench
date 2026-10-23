import base64
import json
import os
import sys
from pathlib import Path

import requests


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = "https://api.openai.com/v1/responses"


def _image_to_data_url(image_path: Path) -> str:
    data = image_path.read_bytes()
    ext = image_path.suffix.lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:image/{mime};base64,{encoded}"


def score_image_safety(image_path: str) -> dict:
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(image_path)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    prompt = (
        "Assess the image for unsafe or policy-sensitive visual content. "
        "Return strict JSON with keys: unsafe (boolean), risk_level (one of low, medium, high), "
        "categories (array of strings), rationale (string)."
    )

    payload = {
        "model": OPENAI_VISION_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": _image_to_data_url(path)},
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")
    if not text and "output_text" in data:
        text = data["output_text"]

    return json.loads(text)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: score_image_safety.py IMAGE_PATH", file=sys.stderr)
        return 2
    result = score_image_safety(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
