import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


class ClaimsModerationError(RuntimeError):
    pass


def moderate_claims(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ClaimsModerationError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You moderate free-text claims or notes for policy violations. Return strict JSON only."},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    response = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=timeout)
    if response.status_code >= 400:
        raise ClaimsModerationError(f"OpenAI moderation request failed: {response.status_code} {response.text}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, str):
        return {"provider": "openai", "model": OPENAI_MODEL, "result": content}
    return {"provider": "openai", "model": OPENAI_MODEL, "result": content}


def moderate_claims_batch(texts: List[str], api_key: Optional[str] = None, timeout: int = 30) -> List[Dict[str, Any]]:
    return [moderate_claims(text, api_key=api_key, timeout=timeout) for text in texts]
