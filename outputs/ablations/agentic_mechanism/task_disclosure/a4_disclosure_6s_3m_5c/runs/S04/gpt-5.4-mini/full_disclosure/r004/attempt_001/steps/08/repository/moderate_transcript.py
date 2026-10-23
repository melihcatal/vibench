import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def moderate_transcript(text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    default_categories = ["hate", "harassment", "sexual", "self-harm", "violence", "illicit"]
    requested_categories = categories or default_categories

    prompt = (
        "Moderate the following transcript for publishing. "
        "Return JSON with keys: flagged (boolean), categories (array of strings), "
        "summary (string), redacted_text (string), and rationale (string). "
        f"Use these categories if relevant: {', '.join(requested_categories)}. "
        "Keep the redacted_text faithful while removing or masking harmful content.\n\n"
        f"Transcript:\n{text}"
    )

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a content moderation assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_MODEL, "result": content}
