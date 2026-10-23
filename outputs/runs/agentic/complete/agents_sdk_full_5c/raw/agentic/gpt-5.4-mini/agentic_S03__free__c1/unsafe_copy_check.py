import os
from typing import Dict

import requests

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"


def check_unsafe_copy(text: str) -> Dict[str, str]:
    api_key = os.getenv(ANTHROPIC_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(f"Missing {ANTHROPIC_API_KEY_ENV}")
    resp = requests.post(
        ANTHROPIC_API_URL,
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={
            "model": ANTHROPIC_MODEL,
            "max_tokens": 128,
            "messages": [{"role": "user", "content": f"Check this localized copy for unsafe content: {text}"}],
        },
        timeout=30,
    )
    resp.raise_for_status()
    return {"result": resp.json()["content"][0]["text"]}
