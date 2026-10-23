import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL_ID = "gpt-4.1-mini"


def check_message_safety(message_payload: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    text = str(message_payload.get("text", ""))
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Assess whether the following message text contains unsafe content such as violence, self-harm, "
        "hate, sexual content involving minors, fraud, or instructions for wrongdoing. Return JSON with "
        'keys "unsafe" (boolean), "categories" (array of strings), and "reason" (string). Text: '
        + text
    )

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL_ID,
            "messages": [
                {"role": "system", "content": "You are a message safety classifier."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_MODEL_ID, "result": content}
