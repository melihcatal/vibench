import json
import os
from typing import Any, Dict

import requests


OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def translate_onboarding_copy(copy: str, locale: str | None = None) -> str:
    target_locale = locale or os.getenv("USER_LOCALE") or os.getenv("LANG", "en").split(".")[0].split("_")[0]
    if target_locale.startswith("en"):
        return copy

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for translation")

    payload: Dict[str, Any] = {
        "model": OPENAI_TRANSLATION_MODEL,
        "messages": [
            {"role": "system", "content": "You translate onboarding copy accurately and naturally."},
            {
                "role": "user",
                "content": json.dumps({"locale": target_locale, "copy": copy}, ensure_ascii=False),
            },
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    onboarding_copy = os.getenv("ONBOARDING_COPY", "Welcome! Let's get you set up.")
    print(translate_onboarding_copy(onboarding_copy))


if __name__ == "__main__":
    main()
