import base64
import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_DEFAULT_MODEL = "gpt-5.4-mini"


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".") or "png"
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64,{encoded}"


def extract_text(image_path: str, api_key: Optional[str] = None, model: str = OPENAI_DEFAULT_MODEL) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract the plain text from this scanned document image. Return only the text."},
                    {"type": "input_image", "image_url": _image_to_data_url(image_path)},
                ],
            }
        ],
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    texts = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text"):
                texts.append(content.get("text", ""))
    return "\n".join(t for t in texts if t).strip()
