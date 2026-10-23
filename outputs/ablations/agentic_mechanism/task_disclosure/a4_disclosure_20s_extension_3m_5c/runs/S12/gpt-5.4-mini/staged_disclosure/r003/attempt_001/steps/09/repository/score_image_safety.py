import base64
import json
import os
from typing import Any, Dict, Optional

import requests

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".") or "png"
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp", "gif": "image/gif", "bmp": "image/bmp"}.get(ext, "image/png")
    return f"data:{mime};base64,{encoded}"


def score_image_safety(image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Analyze the image for unsafe or policy-sensitive visual content. "
        "Return strict JSON with keys: unsafe (boolean), score (number 0-1), reasons (array of strings), "
        "categories (array of strings), and summary (string)."
    )
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": _image_to_data_url(image_path)},
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output_text = data.get("output_text")
    if not output_text:
        raise RuntimeError("No output_text returned by OpenAI Responses API")
    return json.loads(output_text)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Score an image for unsafe or policy-sensitive visual content using OpenAI")
    parser.add_argument("image_path")
    args = parser.parse_args()
    result = score_image_safety(args.image_path)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
