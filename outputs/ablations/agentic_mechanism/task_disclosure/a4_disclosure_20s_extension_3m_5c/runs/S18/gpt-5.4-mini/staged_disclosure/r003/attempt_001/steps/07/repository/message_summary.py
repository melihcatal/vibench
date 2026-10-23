import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(messages: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = ["Summarize the following message processing results concisely."]
    for index, message in enumerate(messages, start=1):
        lines.append(f"{index}. {message}")
    return "\n".join(lines)


def summarize_message_results(messages: Iterable[Dict[str, Any]], api_key: Optional[str] = None) -> str:
    token = api_key or os.environ.get("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You summarize message processing results."},
            {"role": "user", "content": _build_prompt(messages)},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def summarize_message_processing_results(messages: Iterable[Dict[str, Any]], api_key: Optional[str] = None) -> str:
    return summarize_message_results(messages, api_key=api_key)
