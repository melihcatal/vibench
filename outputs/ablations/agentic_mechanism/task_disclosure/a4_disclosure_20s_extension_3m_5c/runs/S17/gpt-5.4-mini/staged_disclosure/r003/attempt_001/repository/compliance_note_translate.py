import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_compliance_note(text: str, target_language: str = "en") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Translate the following encryption or compliance note for reviewers. "
        "Preserve technical meaning, policy terms, and any warnings. Return only the translation.\n\n"
        f"Target language: {target_language}\n\n"
        f"Note:\n{text}"
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
                {"role": "system", "content": "You translate compliance and encryption notes accurately."},
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
        raise SystemExit("Usage: compliance_note_translate.py <note> [target_language]")

    note = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "en"
    print(translate_compliance_note(note, target_language))


if __name__ == "__main__":
    main()
