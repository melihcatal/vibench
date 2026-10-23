import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_IMAGE_SAFETY_MODEL = os.getenv("OPENAI_IMAGE_SAFETY_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


@dataclass
class SafetyScore:
    unsafe: bool
    score: float
    categories: Dict[str, bool]
    summary: str
    raw: Dict[str, Any]


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext or "png"
    return f"data:image/{mime};base64,{encoded}"


def score_image_safety(image_path: str) -> SafetyScore:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_IMAGE_SAFETY_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You assess whether an image contains unsafe or policy-sensitive visual content. "
                    "Return strict JSON with keys: unsafe (boolean), score (number from 0 to 1, higher means more unsafe), "
                    "categories (object with booleans for nudity, sexual_content, violence, self_harm, hate_symbols, minors, weapons, drugs, other), "
                    "and summary (short string)."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this image for safety policy sensitivity."},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
                ],
            },
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    return SafetyScore(
        unsafe=bool(parsed.get("unsafe", False)),
        score=float(parsed.get("score", 0.0)),
        categories=dict(parsed.get("categories", {})),
        summary=str(parsed.get("summary", "")),
        raw=parsed,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Score image safety using OpenAI vision.")
    parser.add_argument("image_path")
    args = parser.parse_args()

    result = score_image_safety(args.image_path)
    print(json.dumps(result.raw, ensure_ascii=False))
