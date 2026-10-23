import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def moderate_claims(text: str, extra_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = (
        "You are a moderation assistant for free-text claims or notes. "
        "Classify the text for safety, abuse, fraud, harassment, hate, self-harm, sexual content, "
        "and sensitive personal data. Return concise JSON with fields: "
        "flagged (boolean), categories (array of strings), severity (low|medium|high), summary (string), rationale (string)."
    )

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text if not extra_context else f"Text: {text}\nContext: {extra_context}"},
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
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_MODEL, "result": content}


def moderate_claims_batch(texts: List[str]) -> List[Dict[str, Any]]:
    return [moderate_claims(text) for text in texts]
