from __future__ import annotations

import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_alt_text(text: str, target_language: str = "es", api_key: Optional[str] = None, model: str = OPENAI_MODEL) -> str:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    if not text:
        return ""

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You translate short image descriptions accurately and naturally. Preserve meaning, tone, and any visible text references.",
            },
            {
                "role": "user",
                "content": f"Translate the following image description into {target_language}. Return only the translation:\n\n{text}",
            },
        ],
        "temperature": 0,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate generated image descriptions using OpenAI.")
    parser.add_argument("text")
    parser.add_argument("--target-language", default="es")
    args = parser.parse_args()
    print(translate_alt_text(args.text, target_language=args.target_language))


if __name__ == "__main__":
    main()
