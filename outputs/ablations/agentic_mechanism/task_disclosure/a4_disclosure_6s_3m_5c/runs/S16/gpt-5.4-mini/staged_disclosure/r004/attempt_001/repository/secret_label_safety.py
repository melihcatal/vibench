import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(secret_label: str, secret_notes: str) -> str:
    return (
        "Check the following secret label and notes for unsafe text. "
        "Flag content that is malicious, social-engineering oriented, credential-harvesting, "
        "self-harm related, violent, hateful, sexually explicit, or otherwise unsafe. "
        "Return valid JSON with keys: unsafe (boolean), reasons (array of strings), "
        "and sanitized_text (string).\n\n"
        f"secret_label: {secret_label}\n"
        f"secret_notes: {secret_notes}"
    )


def check_secret_label_safety(secret_label: str, secret_notes: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(secret_label, secret_notes),
        "temperature": 0,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    text: Optional[str] = None
    if isinstance(data, dict):
        output = data.get("output", [])
        for item in output:
            content = item.get("content", []) if isinstance(item, dict) else []
            for block in content:
                if isinstance(block, dict) and block.get("type") in {"output_text", "text"}:
                    text = block.get("text")
                    if text:
                        break
            if text:
                break

    if not text:
        raise ValueError("OpenAI response did not include text output")

    import json

    return json.loads(text)


def main() -> None:
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: secret_label_safety.py <secret_label> <secret_notes>")

    result = check_secret_label_safety(sys.argv[1], sys.argv[2])
    print(result)


if __name__ == "__main__":
    main()
