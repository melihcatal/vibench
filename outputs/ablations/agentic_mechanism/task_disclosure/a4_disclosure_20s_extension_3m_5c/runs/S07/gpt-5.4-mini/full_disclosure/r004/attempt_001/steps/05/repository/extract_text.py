import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


def _image_to_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def extract_text_from_document_image(image_bytes: bytes, mime_type: str = "image/png", extra_instructions: Optional[str] = None) -> str:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = "Extract plain text from this scanned document image. Preserve reading order and line breaks."
    if extra_instructions:
        prompt = f"{prompt} {extra_instructions}"

    payload: Dict[str, Any] = {
        "model": OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_bytes, mime_type)}},
                ],
            }
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def extract_text_from_file(path: str, mime_type: Optional[str] = None, extra_instructions: Optional[str] = None) -> str:
    with open(path, "rb") as f:
        image_bytes = f.read()
    if mime_type is None:
        lower = path.lower()
        if lower.endswith(".jpg") or lower.endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif lower.endswith(".webp"):
            mime_type = "image/webp"
        else:
            mime_type = "image/png"
    return extract_text_from_document_image(image_bytes, mime_type=mime_type, extra_instructions=extra_instructions)
