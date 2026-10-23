import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def moderate_claim(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Moderate the following free-text claim or note for policy violations, safety risks, "
        "fraud indicators, harassment, self-harm, violence, illegal activity, sexual content, "
        "and medical/legal misinformation. Return strict JSON with keys: decision, categories, "
        "severity, rationale, red_flags. decision must be one of allow, review, or block.\n\n"
        f"Text: {text}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a strict moderation classifier."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_MODEL, "result": content}


def moderate_claims(texts: List[str]) -> List[Dict[str, Any]]:
    return [moderate_claim(text) for text in texts]


def moderate_note(text: str) -> Dict[str, Any]:
    return moderate_claim(text)
