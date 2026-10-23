import base64
import json
import mimetypes
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")


def _load_image_as_data_url(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def score_image_safety(image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    image_url = _load_image_as_data_url(image_path)
    payload = {
        "model": OPENAI_SAFETY_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this image for unsafe or policy-sensitive visual content. "
                            "Return JSON with keys: safe (boolean), severity (string), categories (array of strings), "
                            "rationale (string), and confidence (number from 0 to 1)."
                        ),
                    },
                    {"type": "image_url", "image_url": {"url": image_url}},
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
    return {
        "provider": "openai",
        "model": OPENAI_SAFETY_MODEL,
        "safe": bool(parsed.get("safe", False)),
        "severity": parsed.get("severity", "unknown"),
        "categories": parsed.get("categories", []),
        "rationale": parsed.get("rationale", ""),
        "confidence": parsed.get("confidence", 0),
        "raw": parsed,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Score an image for unsafe or policy-sensitive visual content using OpenAI.")
    parser.add_argument("image_path")
    args = parser.parse_args()
    print(json.dumps(score_image_safety(args.image_path), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
