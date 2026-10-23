import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(record: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key in ("title", "name", "summary", "content", "body", "text", "description"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    if not parts:
        parts.append(str(record))
    return "\n".join(parts)


def summarize_records(records: List[Dict[str, Any]]) -> str:
    if not records:
        return "No records to summarize."

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = "Summarize these retrieved document records into a concise paragraph highlighting key themes, important facts, and any notable differences.\n\n"
    for index, record in enumerate(records, start=1):
        prompt += f"Record {index}:\n{_extract_text(record)}\n\n"

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize document records clearly and succinctly."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    raise SystemExit("Import summarize_records and pass retrieved document records.")
