import base64
import json
import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _encode_image_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext or "png"
    return f"data:image/{mime};base64,{encoded}"


def score_image_safety(image_path: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Analyze this image for unsafe or policy-sensitive visual content. "
        "Return ONLY valid JSON with keys: safe (boolean), score (number from 0 to 1 where 1 is most unsafe), "
        "categories (array of short strings), and rationale (short string). "
        "Use categories such as violence, sexual_content, self_harm, hate, illegal_activity, or other relevant labels."
    )
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _encode_image_data_url(image_path)}},
                ],
            }
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()
    result = json.loads(content)
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object response")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    args = parser.parse_args()
    print(json.dumps(score_image_safety(args.image_path)))
