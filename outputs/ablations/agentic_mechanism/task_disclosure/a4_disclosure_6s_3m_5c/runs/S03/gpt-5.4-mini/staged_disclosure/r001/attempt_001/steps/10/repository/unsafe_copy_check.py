import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("text", "content", "copy", "localized_copy", "localizedCopy"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
        for key in ("items", "messages", "segments", "strings"):
            value = payload.get(key)
            if isinstance(value, list):
                parts = []
                for item in value:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        for nested_key in ("text", "content", "copy"):
                            nested_value = item.get(nested_key)
                            if isinstance(nested_value, str):
                                parts.append(nested_value)
                                break
                if parts:
                    return "\n".join(parts)
    raise ValueError("Could not extract localized copy from input")


def check_unsafe_copy(localized_copy: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "You are a safety checker for localized marketing and product copy. "
        "Identify unsafe content such as hate, harassment, sexual content, self-harm encouragement, "
        "violent wrongdoing, fraud, illegal advice, privacy invasion, or manipulative/deceptive claims. "
        "Return strict JSON with keys: unsafe (boolean), categories (array of strings), reasons (array of strings). "
        "If safe, unsafe must be false and categories/reasons must be empty arrays.\n\n"
        f"COPY:\n{localized_copy}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: unsafe_copy_check.py '<localized copy>' or JSON via stdin"}))
        return 1

    raw_input = " ".join(sys.argv[1:]).strip()
    if raw_input == "-":
        raw_input = sys.stdin.read().strip()

    try:
        payload = json.loads(raw_input)
        localized_copy = _extract_text(payload)
    except json.JSONDecodeError:
        localized_copy = raw_input

    result = check_unsafe_copy(localized_copy)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
