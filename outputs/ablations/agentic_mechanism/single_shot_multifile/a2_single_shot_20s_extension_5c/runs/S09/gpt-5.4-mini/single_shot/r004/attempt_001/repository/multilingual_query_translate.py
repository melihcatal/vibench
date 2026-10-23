import os
from typing import Dict

import requests


OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


def multilingual_query_translate(query: str, target_language: str = "en") -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    url = f"{base_url}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": OPENAI_CHAT_MODEL,
        "messages": [
            {"role": "system", "content": f"Translate the user's query into {target_language}."},
            {"role": "user", "content": query},
        ],
        "temperature": 0,
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    translated = response.json()["choices"][0]["message"]["content"].strip()
    return {"provider": "openai", "model": OPENAI_CHAT_MODEL, "translated_query": translated}


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read())
    print(json.dumps(multilingual_query_translate(payload["query"], payload.get("target_language", "en"))))
