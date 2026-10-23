import os
from typing import List

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_API_HOST = "https://api.openai.com/v1/chat/completions"


def summarize_quality_issues(translated_text: str, source_text: str) -> List[str]:
    api_key = os.getenv(OPENAI_API_KEY_ENV, "")
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Summarize translation quality issues briefly."},
            {"role": "user", "content": f"Source: {source_text}\nTranslation: {translated_text}"},
        ],
        "temperature": 0.2,
    }
    response = requests.post(OPENAI_API_HOST, headers={"Authorization": f"Bearer {api_key}"}, json=payload, timeout=30)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return [line.strip("- ") for line in content.splitlines() if line.strip()]
