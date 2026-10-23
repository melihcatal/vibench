import json
import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_customer_message_payload(payload: Dict[str, Any], target_language: str = "en") -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    messages = [
        {
            "role": "system",
            "content": "Translate only customer-facing message text fields in the provided JSON payload to the target language while preserving keys, structure, and non-text values.",
        },
        {
            "role": "user",
            "content": json.dumps({"target_language": target_language, "payload": payload}, ensure_ascii=False),
        },
    ]

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)
