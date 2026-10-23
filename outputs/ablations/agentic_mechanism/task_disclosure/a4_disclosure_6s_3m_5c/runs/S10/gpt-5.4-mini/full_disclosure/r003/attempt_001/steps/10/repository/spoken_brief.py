import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_SPOKEN_BRIEF_MODEL", "gpt-4o-mini")


def _build_messages(model_output: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You turn model output into a short spoken brief that sounds natural when read aloud.",
        },
        {
            "role": "user",
            "content": f"Rewrite the following model output as a concise spoken brief. Keep it clear, conversational, and easy to read aloud:\n\n{model_output}",
        },
    ]


def generate_spoken_brief(model_output: str, api_key: Optional[str] = None, model: Optional[str] = None, temperature: float = 0.3, max_tokens: int = 180) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload: Dict[str, Any] = {
        "model": model or OPENAI_MODEL,
        "messages": _build_messages(model_output),
        "temperature": temperature,
        "max_tokens": max_tokens,
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
