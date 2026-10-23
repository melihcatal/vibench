import os
from typing import Iterable, List

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def summarize_meeting_chunks(chunks: Iterable[str]) -> str:
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())
    if not transcript:
        return ""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Summarize live meeting transcript chunks into concise notes with key decisions, action items, and open questions.",
                },
                {"role": "user", "content": transcript},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
