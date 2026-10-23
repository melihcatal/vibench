import os
from typing import List, Dict, Any

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_compliance_notes(notes: str, target_language: str = "English") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Translate encryption or compliance notes for reviewers accurately and concisely.",
            },
            {
                "role": "user",
                "content": f"Translate the following notes into {target_language}:\n\n{notes}",
            },
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    choices: List[Dict[str, Any]] = data.get("choices", [])
    if not choices:
        raise RuntimeError("No translation returned")
    message = choices[0].get("message", {})
    content = message.get("content")
    if not content:
        raise RuntimeError("Empty translation returned")
    return content.strip()
