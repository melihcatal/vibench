import base64
import json
import mimetypes
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _load_image_as_data_url(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def detect_image_labels(image_path: str, max_labels: int = 10, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    image_url = _load_image_as_data_url(image_path)
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Identify the main labels or objects in this image. "
                            f"Return at most {max_labels} items as JSON array of objects with fields label and confidence."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    labels = parsed.get("labels", parsed.get("items", parsed if isinstance(parsed, list) else []))
    if isinstance(labels, dict):
        labels = [labels]
    return labels[:max_labels]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Detect labels or objects in a static image using OpenAI.")
    parser.add_argument("image_path")
    parser.add_argument("--max-labels", type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(detect_image_labels(args.image_path, args.max_labels), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
