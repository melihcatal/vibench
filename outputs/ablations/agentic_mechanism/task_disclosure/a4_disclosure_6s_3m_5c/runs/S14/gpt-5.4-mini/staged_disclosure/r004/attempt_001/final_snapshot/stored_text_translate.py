import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_stored_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = "Translate the provided text accurately and preserve meaning, formatting, and tone. Return only the translated text."
    user_payload: Dict[str, Any] = {
        "text": text,
        "target_language": target_language,
    }
    if source_language:
        user_payload["source_language"] = source_language

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
                ],
                "temperature": 0,
            }
        ),
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"].strip()


def main() -> None:
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: stored_text_translate.py <target_language> <text> [source_language]")

    target_language = sys.argv[1]
    text = sys.argv[2]
    source_language = sys.argv[3] if len(sys.argv) > 3 else None
    print(translate_stored_text(text=text, target_language=target_language, source_language=source_language))


if __name__ == "__main__":
    main()
