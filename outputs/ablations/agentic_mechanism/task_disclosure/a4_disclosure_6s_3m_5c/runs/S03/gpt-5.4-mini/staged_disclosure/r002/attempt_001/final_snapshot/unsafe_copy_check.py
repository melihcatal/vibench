import os
import sys
import json
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def check_unsafe_copy(copy_text: str, locale: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_instructions = (
        "You are a safety classifier for localized marketing copy. "
        "Assess whether the provided copy contains unsafe content such as hate, harassment, "
        "sexual content, self-harm encouragement, illegal wrongdoing, or deceptive claims. "
        "Return strict JSON with keys: unsafe (boolean), category (string), rationale (string)."
    )
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_instructions}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps({"locale": locale, "copy": copy_text}, ensure_ascii=False),
                    }
                ],
            },
        ],
        "text": {"format": {"type": "json_object"}},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data.get("output", [{}])[0].get("content", [{}])[0].get("text", "{}")
    return json.loads(text)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: unsafe_copy_check.py <copy> [locale]", file=sys.stderr)
        return 2
    copy_text = sys.argv[1]
    locale = sys.argv[2] if len(sys.argv) > 2 else None
    result = check_unsafe_copy(copy_text, locale)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
