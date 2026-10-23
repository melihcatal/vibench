import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lstrip(".").lower() or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def score_image_safety(image_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    user_prompt = prompt or (
        "Assess the image for unsafe or policy-sensitive visual content. "
        "Return strict JSON with keys: safe (boolean), categories (array of strings), "
        "risk_score (number from 0 to 1), and rationale (string)."
    )

    payload = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
                ],
            }
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        f"{OPENAI_API_BASE}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("--prompt", default=None)
    args = parser.parse_args()
    result = score_image_safety(args.image_path, args.prompt)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
