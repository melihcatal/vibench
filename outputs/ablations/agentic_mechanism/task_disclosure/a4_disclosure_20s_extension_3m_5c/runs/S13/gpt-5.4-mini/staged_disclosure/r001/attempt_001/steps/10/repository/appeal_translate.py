import os
import sys
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_appeal_text(text: str, target_language: str = "English") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        f"Translate the following appeal text into {target_language}. "
        "Preserve meaning, tone, and any relevant formatting. Return only the translation.\n\n"
        f"{text}"
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
                {"role": "system", "content": "You are a professional translation assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main(argv: Optional[list[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return 1

    text = " ".join(args)
    translated = translate_appeal_text(text)
    sys.stdout.write(translated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
