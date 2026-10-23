import os
from typing import List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_runbook_notes(notes: str, target_language: str = "Spanish") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Translate secret-rotation runbook notes accurately, preserving bullets, code, secrets markers, and operational meaning.",
            },
            {
                "role": "user",
                "content": f"Translate the following runbook notes to {target_language}:\n\n{notes}",
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
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def _read_stdin() -> str:
    import sys

    return sys.stdin.read()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate secret-rotation runbook notes using OpenAI.")
    parser.add_argument("--target-language", default="Spanish")
    args = parser.parse_args()
    notes = _read_stdin()
    if not notes.strip():
        raise SystemExit("No input provided on stdin")
    print(translate_runbook_notes(notes, args.target_language))


if __name__ == "__main__":
    main()
