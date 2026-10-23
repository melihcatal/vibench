import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(label: str, note: str) -> str:
    return (
        "Check the following secret label and note for unsafe text. "
        "Unsafe text includes secrets, credentials, tokens, passwords, "
        "malware instructions, exfiltration guidance, or abusive content. "
        "Return JSON with keys unsafe (boolean), reasons (array of strings), and summary (string).\n\n"
        f"Label: {label}\n"
        f"Note: {note}"
    )


def check_secret_label_safety(label: str, note: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a safety classifier."},
                {"role": "user", "content": _build_prompt(label, note)},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("note")
    args = parser.parse_args()
    print(json.dumps(check_secret_label_safety(args.label, args.note), ensure_ascii=False))


if __name__ == "__main__":
    main()
