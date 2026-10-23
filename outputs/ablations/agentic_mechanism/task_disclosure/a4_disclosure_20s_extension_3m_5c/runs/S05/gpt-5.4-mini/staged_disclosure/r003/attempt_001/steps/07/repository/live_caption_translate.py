import json
import os
import sys
from typing import Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_caption(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_message = (
        "You translate live captions faithfully and concisely. "
        "Preserve meaning, punctuation, speaker labels, and line breaks. "
        "Return only the translation."
    )
    user_message = f"Translate the following caption into {target_language}."
    if source_language:
        user_message += f" The source language is {source_language}."
    user_message += f"\n\n{text}"

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python live_caption_translate.py <target_language> <caption_text> [source_language]", file=sys.stderr)
        return 1

    target_language = sys.argv[1]
    caption_text = sys.argv[2]
    source_language = sys.argv[3] if len(sys.argv) > 3 else None
    print(translate_caption(caption_text, target_language, source_language))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
