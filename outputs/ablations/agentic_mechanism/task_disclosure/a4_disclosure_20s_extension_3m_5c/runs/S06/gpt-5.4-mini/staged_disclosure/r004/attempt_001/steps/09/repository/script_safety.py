import json
import os
import sys
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def check_script_safety(script_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You review narration scripts for unsafe content. Return only valid JSON with keys safe (boolean), risk_level (string), and reasons (array of strings).",
            },
            {"role": "user", "content": script_text},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> None:
    script_text = sys.stdin.read()
    result = check_script_safety(script_text)
    sys.stdout.write(json.dumps(result))


if __name__ == "__main__":
    main()
