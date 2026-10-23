import os
from typing import Optional

import requests


OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def translate_platform_output(text: str, target_locale: str = "en") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        f"Translate the following platform model output into {target_locale}. "
        "Preserve meaning, formatting, code snippets, identifiers, and placeholders. "
        "Return only the translated text.\n\n"
        f"{text}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TRANSLATION_MODEL,
            "messages": [
                {"role": "system", "content": "You are a precise translation engine."},
                {"role": "user", "content": prompt},
            ],
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
        raise SystemExit("Usage: python localized_platform_output.py <text> [locale]")

    text = sys.argv[1]
    locale = sys.argv[2] if len(sys.argv) > 2 else "en"
    print(translate_platform_output(text, locale))


if __name__ == "__main__":
    main()
