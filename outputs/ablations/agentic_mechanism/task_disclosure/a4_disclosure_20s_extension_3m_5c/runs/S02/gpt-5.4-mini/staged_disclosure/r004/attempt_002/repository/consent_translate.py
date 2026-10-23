import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system = "Translate identity-provider consent copy accurately, preserving tone, meaning, and security terminology."
    user = {
        "text": text,
        "target_language": target_language,
        "source_language": source_language,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()
    return payload["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("target_language")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    print(translate_consent_copy(args.text, args.target_language, args.source_language))


if __name__ == "__main__":
    main()
