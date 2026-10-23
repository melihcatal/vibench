import argparse
import os
import sys
from typing import Any

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def translate_script(text: str, target_language: str, source_language: str | None = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = (
        "You translate narration scripts for speech synthesis. "
        "Preserve line breaks, timing cues, punctuation style, and markup. "
        "Return only the translated script."
    )
    user_prompt = f"Translate this script into {target_language}."
    if source_language:
        user_prompt += f" Source language: {source_language}."
    user_prompt += f"\n\n{text}"

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate narration scripts before synthesis.")
    parser.add_argument("--target-language", required=True)
    parser.add_argument("--source-language")
    parser.add_argument("input", nargs="?", help="Input file path; reads stdin if omitted")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    translated = translate_script(text, args.target_language, args.source_language)
    sys.stdout.write(translated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
