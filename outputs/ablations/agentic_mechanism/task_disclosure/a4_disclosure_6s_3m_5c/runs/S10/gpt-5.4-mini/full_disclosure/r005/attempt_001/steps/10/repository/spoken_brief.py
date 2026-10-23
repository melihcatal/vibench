import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _auth_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _build_messages(model_output: str) -> List[Dict[str, str]]:
    system = (
        "You convert model output into a concise spoken brief. "
        "Write in natural, clear speech suitable for reading aloud. "
        "Keep it brief, fluent, and faithful to the original meaning."
    )
    user = f"Model output:\n{model_output}\n\nCreate a spoken brief."
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def generate_spoken_brief(model_output: str, temperature: float = 0.3, max_tokens: int = 120) -> str:
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": _build_messages(model_output),
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    response = requests.post(OPENAI_CHAT_COMPLETIONS_URL, headers=_auth_headers(), json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
