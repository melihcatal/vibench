import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_alt_text(text: str, target_language: str = "en") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You translate image descriptions accurately while preserving meaning and concise alt-text style.",
            },
            {
                "role": "user",
                "content": f"Translate the following alt text into {target_language}: {text}",
            },
        ],
        "temperature": 0,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--target-language", default="en")
    args = parser.parse_args()
    print(translate_alt_text(args.text, args.target_language))


if __name__ == "__main__":
    main()
