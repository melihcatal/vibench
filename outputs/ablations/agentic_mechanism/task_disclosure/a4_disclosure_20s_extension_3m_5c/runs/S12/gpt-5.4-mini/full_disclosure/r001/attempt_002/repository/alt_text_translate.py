import os
from typing import Optional

import requests


OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def translate_alt_text(description: str, target_language: str, source_language: Optional[str] = None) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    messages = [
        {
            "role": "system",
            "content": "You translate image descriptions accurately and naturally while preserving meaning, tone, and brevity.",
        },
        {
            "role": "user",
            "content": _build_prompt(description, target_language, source_language),
        },
    ]

    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def _build_prompt(description: str, target_language: str, source_language: Optional[str]) -> str:
    parts = [
        f"Translate the following image description into {target_language}.",
    ]
    if source_language:
        parts.append(f"The source language is {source_language}.")
    parts.append("Return only the translated description.")
    parts.append("")
    parts.append(description)
    return "\n".join(parts)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("description")
    parser.add_argument("target_language")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    print(translate_alt_text(args.description, args.target_language, args.source_language))


if __name__ == "__main__":
    main()
