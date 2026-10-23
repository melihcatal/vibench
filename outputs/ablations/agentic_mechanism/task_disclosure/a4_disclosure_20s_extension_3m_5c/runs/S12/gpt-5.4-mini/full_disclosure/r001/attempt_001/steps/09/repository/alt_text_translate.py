import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


def _build_payload(text: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
    source_clause = f" from {source_language}" if source_language else ""
    return {
        "model": DEFAULT_MODEL,
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": "You translate short image descriptions accurately and concisely.",
            },
            {
                "role": "user",
                "content": (
                    f"Translate this image description{source_clause} into {target_language}. "
                    f"Return only the translated text.\n\nDescription: {text}"
                ),
            },
        ],
    }


def translate_alt_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=_build_payload(text, target_language, source_language),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate generated image descriptions")
    parser.add_argument("text")
    parser.add_argument("target_language")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    print(translate_alt_text(args.text, args.target_language, args.source_language))


if __name__ == "__main__":
    main()
