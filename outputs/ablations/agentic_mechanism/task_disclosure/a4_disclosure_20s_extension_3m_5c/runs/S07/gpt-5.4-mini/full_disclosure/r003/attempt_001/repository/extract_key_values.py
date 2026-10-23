import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/responses")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_KEY_VALUE_MODEL = os.getenv("OPENAI_KEY_VALUE_MODEL", "gpt-4.1-mini")


def _encode_image(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def extract_key_values(image_bytes: bytes, mime_type: str = "image/png", instruction: Optional[str] = None) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = instruction or "Extract key-value pairs from this form-like document and return JSON with a key_values object mapping field names to values. Preserve the original labels and values as faithfully as possible."
    payload = {
        "model": OPENAI_KEY_VALUE_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": f"data:{mime_type};base64,{_encode_image(image_bytes)}"},
                ],
            }
        ],
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=120)
    response.raise_for_status()
    data = response.json()

    text = None
    if isinstance(data, dict):
        if data.get("output_text"):
            text = data["output_text"]
        elif data.get("output"):
            for item in data["output"]:
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"}:
                        text = content.get("text")
                        break
                if text:
                    break

    if not text:
        return data

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"key_values": {}, "raw_text": text, "provider_response": data}
