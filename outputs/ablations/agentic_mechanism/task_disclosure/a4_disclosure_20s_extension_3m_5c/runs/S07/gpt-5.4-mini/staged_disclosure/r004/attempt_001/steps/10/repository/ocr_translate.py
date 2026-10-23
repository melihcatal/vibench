import os
import json
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def translate_ocr_text(text: str, target_language: str = "en", source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    system_prompt = "You are a translation engine. Translate OCR text accurately and preserve layout as much as possible."
    user_prompt = {
        "target_language": target_language,
        "source_language": source_language,
        "text": text,
    }

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
                    {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
                ],
                "temperature": 0,
            }
        ),
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python ocr_translate.py <text> [target_language]")

    text = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "en"
    print(translate_ocr_text(text, target_language=target_language))
