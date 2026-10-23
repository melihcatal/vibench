import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _normalize_messages(messages: List[Dict[str, Any]]) -> str:
    lines = []
    for item in messages:
        role = str(item.get("role", ""))
        content = item.get("content", "")
        if isinstance(content, list):
            content = " ".join(str(part.get("text", part)) for part in content)
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def summarize_message_processing_results(messages: List[Dict[str, Any]], max_tokens: int = 200) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Summarize the message processing results concisely. "
        "Focus on successes, failures, and notable patterns.\n\n"
        f"{_normalize_messages(messages)}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize message processing results."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def summarize_results(messages: List[Dict[str, Any]]) -> str:
    return summarize_message_processing_results(messages)


def main() -> None:
    raise SystemExit("Import and call summarize_message_processing_results with message data.")


if __name__ == "__main__":
    main()
