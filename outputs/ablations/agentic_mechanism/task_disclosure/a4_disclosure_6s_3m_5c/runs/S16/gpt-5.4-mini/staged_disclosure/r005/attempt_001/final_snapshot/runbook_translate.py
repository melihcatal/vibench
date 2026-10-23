import os
import json
from typing import List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_messages(notes: str, target_language: str) -> List[dict]:
    return [
        {
            "role": "system",
            "content": "Translate secret-rotation runbook notes accurately, preserving security-sensitive terminology, step ordering, and any imperative language.",
        },
        {
            "role": "user",
            "content": f"Translate the following runbook notes into {target_language}:\n\n{notes}",
        },
    ]


def translate_runbook_notes(notes: str, target_language: str = "English") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(notes, target_language),
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: runbook_translate.py <notes-file> [target-language]")
    notes_path = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "English"
    with open(notes_path, "r", encoding="utf-8") as handle:
        notes = handle.read()
    print(translate_runbook_notes(notes, target_language))


if __name__ == "__main__":
    main()
