import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(copy_text: str, locale: Optional[str] = None) -> str:
    locale_part = f"Locale: {locale}\n" if locale else ""
    return (
        "Review the localized marketing copy for unsafe content. "
        "Flag content that is deceptive, hateful, harassing, sexual, violent, or otherwise unsafe. "
        "Return strict JSON with keys: unsafe (boolean), reasons (array of strings), cleaned_copy (string).\n"
        f"{locale_part}Copy:\n{copy_text}"
    )


def check_unsafe_copy(copy_text: str, locale: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a safety reviewer for localized copy."},
            {"role": "user", "content": _build_prompt(copy_text, locale)},
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_MODEL, "result": content}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Check localized copy for unsafe content.")
    parser.add_argument("copy_text")
    parser.add_argument("--locale", default=None)
    args = parser.parse_args()
    result = check_unsafe_copy(args.copy_text, args.locale)
    print(result)


if __name__ == "__main__":
    main()
