import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def moderate_vendor_text_safety(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": "You are a text safety moderator for vendor notes and memo fields. Return strict JSON with keys: allow (boolean), category (string), reason (string), redacted_text (string).",
            },
            {"role": "user", "content": text},
        ],
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)
