import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_stored_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = "You are a professional translation engine. Return only the translated text."
    user_prompt = f"Translate the following text into {target_language}."
    if source_language:
        user_prompt += f" The source language is {source_language}."
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
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", default=sys.stdin.read())
    parser.add_argument("--target-language", required=True)
    parser.add_argument("--source-language")
    args = parser.parse_args()
    print(translate_stored_text(args.text, args.target_language, args.source_language))


if __name__ == "__main__":
    main()
