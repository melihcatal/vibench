import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_consent_copy(
    text: str,
    target_language: str,
    api_key: Optional[str] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    if not text:
        raise ValueError("text is required")
    if not target_language:
        raise ValueError("target_language is required")

    prompt = (
        "Translate the following identity-provider consent copy into "
        f"{target_language}. Preserve meaning, legal tone, placeholders, and product names. "
        "Return strict JSON with keys: translated_text (string), language (string), notes (array of strings). "
        "Text: "
        + text
    )

    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "temperature": 0,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=timeout)
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    if not output_text:
        raise ValueError("No translation response text returned")

    return json.loads(output_text)
