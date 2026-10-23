import os
import base64
from typing import Optional

import requests

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lstrip(".").lower() or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def check_generated_visual_labels_for_unsafe_text(image_path: str, labels: Optional[str] = None) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    content = [
        {"type": "text", "text": "Inspect the visual labels in this image for unsafe, hateful, harassing, sexual, violent, self-harm, or otherwise disallowed text. Return JSON with keys unsafe (boolean), reasons (array of strings), and extracted_text (array of strings). If labels are provided, compare them against the image."},
        {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
    ]
    if labels is not None:
        content.insert(0, {"type": "text", "text": f"Generated labels: {labels}"})

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a safety classifier for visual text content."},
            {"role": "user", "content": content},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0,
    }
    response = requests.post(OPENAI_API_URL, headers={"Authorization": f"Bearer {api_key}"}, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
