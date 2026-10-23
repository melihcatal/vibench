import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You translate appeal text for review. Return only the translated text."
                ),
            },
            {
                "role": "user",
                "content": f"Translate the following appeal text to {target_language}:\n\n{text}",
            },
        ],
        "temperature": 0,
    }

    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: appeal_translate.py <appeal_text> [target_language]")

    text = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "en"
    print(translate_appeal_text(text, target_language))


if __name__ == "__main__":
    main()
