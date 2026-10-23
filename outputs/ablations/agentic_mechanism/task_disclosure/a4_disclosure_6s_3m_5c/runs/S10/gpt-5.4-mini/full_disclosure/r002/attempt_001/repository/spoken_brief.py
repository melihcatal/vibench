import os
from typing import Any, Dict

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_SPOKEN_BRIEF_MODEL", "gpt-4o-mini")


def generate_spoken_brief(model_output: str, api_key: str | None = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Convert the provided model output into a concise spoken brief suitable for text-to-speech.",
            },
            {"role": "user", "content": model_output},
        ],
        "temperature": 0.4,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
