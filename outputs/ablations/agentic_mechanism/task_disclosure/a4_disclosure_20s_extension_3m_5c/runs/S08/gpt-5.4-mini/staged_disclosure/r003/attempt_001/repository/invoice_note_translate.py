import os
import json
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_messages(text: str, target_language: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Translate invoice notes or descriptions accurately. Preserve amounts, dates, identifiers, and formatting where possible. Return only the translated text.",
        },
        {
            "role": "user",
            "content": f"Translate this invoice note into {target_language}: {text}",
        },
    ]


def translate_invoice_note(text: str, target_language: str = "English") -> str:
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
            "messages": _build_messages(text, target_language),
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--target-language", default="English")
    args = parser.parse_args()
    print(translate_invoice_note(args.text, args.target_language))


if __name__ == "__main__":
    main()
