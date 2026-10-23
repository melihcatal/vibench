import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def check_live_caption_safety(text: str) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You assess live transcript text for unsafe content. Return JSON with keys unsafe, category, and rationale.",
            },
            {
                "role": "user",
                "content": f"Analyze this live transcript text for unsafe content and return only JSON:\n\n{text}",
            },
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
