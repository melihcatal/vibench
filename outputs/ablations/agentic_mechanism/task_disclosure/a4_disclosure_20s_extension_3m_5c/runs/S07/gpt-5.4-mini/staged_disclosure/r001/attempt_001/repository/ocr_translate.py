import os
import sys
import json
from typing import List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_ocr_text(text: str, target_language: str = "English") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
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
            "messages": [
                {
                    "role": "system",
                    "content": f"Translate OCR-extracted text into {target_language}. Preserve line breaks, formatting, numbers, and proper nouns when appropriate.",
                },
                {"role": "user", "content": text},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"].strip()


def _read_input(args: List[str]) -> str:
    if len(args) > 1 and args[1] != "-":
        with open(args[1], "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def main() -> None:
    target_language = sys.argv[2] if len(sys.argv) > 2 else "English"
    text = _read_input(sys.argv)
    if not text.strip():
        return
    print(translate_ocr_text(text, target_language))


if __name__ == "__main__":
    main()
