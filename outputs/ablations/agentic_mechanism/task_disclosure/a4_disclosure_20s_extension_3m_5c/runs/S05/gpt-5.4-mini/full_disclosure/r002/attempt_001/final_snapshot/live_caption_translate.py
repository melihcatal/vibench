import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_live_caption(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ["OPENAI_API_KEY"]
    prompt = f"Translate the following live caption into {target_language}. Return only the translated text."
    if source_language:
        prompt = f"Translate the following live caption from {source_language} into {target_language}. Return only the translated text."
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You translate live captions accurately and concisely."},
            {"role": "user", "content": f"{prompt}\n\n{text}"},
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
