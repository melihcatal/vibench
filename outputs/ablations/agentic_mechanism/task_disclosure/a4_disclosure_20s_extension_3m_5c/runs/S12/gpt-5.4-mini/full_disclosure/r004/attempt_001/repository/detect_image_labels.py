import base64
import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_VISION_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_VISION_MODEL = "gpt-4.1-mini"


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext or "png"
    return f"data:image/{mime};base64,{encoded}"


def detect_image_labels(image_path: str, max_labels: int = 10) -> List[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Identify the main objects, entities, and scene labels visible in the image. "
        f"Return at most {max_labels} labels as a JSON array of short strings, with no extra text."
    )
    payload: Dict[str, Any] = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
                ],
            }
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_VISION_ENDPOINT,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    try:
        labels = json.loads(content)
    except json.JSONDecodeError:
        labels = [line.strip("- •\n\t ") for line in content.splitlines() if line.strip()]
    return [str(label) for label in labels][:max_labels]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("--max-labels", type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(detect_image_labels(args.image_path, args.max_labels)))
