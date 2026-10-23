import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_log_messages(messages: List[str], target_locale: str) -> List[str]:
    api_key = os.environ["OPENAI_API_KEY"]
    prompt = {
        "role": "user",
        "content": (
            f"Translate the following support-visible log messages into {target_locale}. "
            "Preserve technical identifiers, codes, timestamps, placeholders, and error tokens exactly. "
            "Return a JSON array of translated strings in the same order. Messages: "
            + str(messages)
        ),
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You translate log messages accurately and conservatively."},
                prompt,
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, list):
        content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    return __import__("json").loads(content)
