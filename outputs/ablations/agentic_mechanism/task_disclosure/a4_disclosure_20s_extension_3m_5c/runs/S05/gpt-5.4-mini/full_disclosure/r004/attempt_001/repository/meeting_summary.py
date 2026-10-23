import os
from typing import Iterable, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


def _normalize_chunks(chunks: Iterable[str]) -> str:
    items: List[str] = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    return "\n".join(f"- {item}" for item in items)


def summarize_meeting_chunks(chunks: Iterable[str], language: str = "English") -> str:
    transcript = _normalize_chunks(chunks)
    if not transcript:
        return ""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You summarize live meeting transcript chunks into a concise, structured meeting summary."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Summarize the following live meeting transcript chunks in {language}. "
                    "Capture key decisions, action items, risks, and open questions.\n\n"
                    f"{transcript}"
                ),
            },
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
