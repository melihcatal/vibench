import json
import os
from typing import List, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _build_prompt(chunks: List[str]) -> str:
    text = "\n\n".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())
    return (
        "You are summarizing a live meeting transcript. "
        "Produce a concise summary with key decisions, action items, open questions, and notable updates.\n\n"
        f"Transcript chunks:\n{text}"
    )


def summarize_meeting_chunks(chunks: List[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, object] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You summarize live meeting transcripts."},
            {"role": "user", "content": _build_prompt(chunks)},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def summarize_live_transcript(chunks: List[str]) -> str:
    return summarize_meeting_chunks(chunks)
