import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "openai/gpt-5.4-mini"


def moderate_claims(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    token = api_key or os.environ.get("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": "You moderate free-text claims or notes for safety, policy violations, and risky content. Return only JSON.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    return {"provider": "openai", "model": OPENAI_MODEL, "result": output_text, "raw": data}


def moderate_claims_batch(texts: List[str], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    return [moderate_claims(text, api_key=api_key) for text in texts]
