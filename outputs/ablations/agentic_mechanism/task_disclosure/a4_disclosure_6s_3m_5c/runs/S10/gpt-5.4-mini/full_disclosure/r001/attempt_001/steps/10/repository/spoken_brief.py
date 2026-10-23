import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def generate_spoken_brief(model_output: str, tone: str = "clear and conversational", max_words: int = 120, api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        f"Rewrite the following model output as a spoken brief in a {tone} style. "
        f"Keep it under about {max_words} words, suitable for being read aloud. "
        f"Preserve the key facts and avoid bullet points unless essential.\n\n"
        f"Model output:\n{model_output}"
    )

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You convert text into short spoken briefs."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 220,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
