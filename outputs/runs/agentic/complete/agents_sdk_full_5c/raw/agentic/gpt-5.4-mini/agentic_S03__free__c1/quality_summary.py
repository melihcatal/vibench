import os
from typing import Dict, List

import requests

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = "gpt-4o-mini"


def summarize_quality(issues: List[str]) -> Dict[str, str]:
    api_key = os.getenv(OPENAI_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(f"Missing {OPENAI_API_KEY_ENV}")
    resp = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Summarize translation quality issues."},
                {"role": "user", "content": "\n".join(issues)},
            ],
        },
        timeout=30,
    )
    resp.raise_for_status()
    return {"summary": resp.json()["choices"][0]["message"]["content"]}
