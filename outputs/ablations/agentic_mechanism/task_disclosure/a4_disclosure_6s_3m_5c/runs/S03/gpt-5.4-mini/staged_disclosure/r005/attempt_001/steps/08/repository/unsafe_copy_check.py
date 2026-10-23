import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(copy_text: str, locale: Optional[str]) -> str:
    locale_part = f"Locale: {locale}\n" if locale else ""
    return (
        "Check the following localized marketing or product copy for unsafe content. "
        "Flag policy-violating, misleading, harmful, or sensitive content, and return a concise JSON object.\n"
        f"{locale_part}"
        f"Copy:\n{copy_text}"
    )


def check_unsafe_copy(copy_text: str, locale: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Return only valid JSON with keys unsafe, reasons, and notes."},
            {"role": "user", "content": _build_prompt(copy_text, locale)},
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("copy_text")
    parser.add_argument("--locale", default=None)
    args = parser.parse_args()
    result = check_unsafe_copy(args.copy_text, args.locale)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
