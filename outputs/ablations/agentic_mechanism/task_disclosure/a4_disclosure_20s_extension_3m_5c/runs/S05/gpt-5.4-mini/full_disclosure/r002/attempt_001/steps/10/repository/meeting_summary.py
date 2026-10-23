import os
from typing import Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4.1-mini"


def _normalize_chunks(chunks: Iterable[str]) -> List[str]:
    return [chunk.strip() for chunk in chunks if chunk and chunk.strip()]


def summarize_meeting_chunks(chunks: Iterable[str], topic: Optional[str] = None) -> str:
    texts = _normalize_chunks(chunks)
    if not texts:
        return ""
    prompt_lines = ["Summarize the following live meeting transcript chunks into concise meeting notes."]
    if topic:
        prompt_lines.append(f"Topic: {topic}")
    prompt_lines.append("Transcript chunks:")
    prompt_lines.extend(f"- {text}" for text in texts)
    payload = {
        "model": os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        "messages": [
            {"role": "system", "content": "You are a helpful meeting summarizer."},
            {"role": "user", "content": "\n".join(prompt_lines)},
        ],
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
