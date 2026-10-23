import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-5.4-mini")


def translate_payload_text(payload_text: str, target_language: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    if not target_language:
        raise ValueError("target_language is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": "Translate customer-facing message payload text accurately while preserving meaning, tone, placeholders, and formatting.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_language}: {payload_text}",
                },
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    translated_text = ""
    if isinstance(data, dict):
        if "output_text" in data and isinstance(data["output_text"], str):
            translated_text = data["output_text"]
        elif data.get("output"):
            chunks = []
            for item in data["output"]:
                for content in item.get("content", []):
                    text = content.get("text")
                    if text:
                        chunks.append(text)
            translated_text = "".join(chunks)

    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "target_language": target_language,
        "translated_text": translated_text,
        "raw": data,
    }
