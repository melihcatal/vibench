import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_appeal_text(text: str, target_language: str = "English", source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = "You translate appeal text for moderation review. Preserve meaning, tone, and any policy-relevant details."
    user_prompt = f"Translate the following appeal text into {target_language}."
    if source_language:
        user_prompt += f" The source language is {source_language}."
    user_prompt += f" Return only the translated text.\n\n{text}"

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
    data: Dict[str, Any] = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: appeal_translate.py TEXT [TARGET_LANGUAGE]")
    text = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "English"
    print(translate_appeal_text(text, target_language=target_language))


if __name__ == "__main__":
    main()
