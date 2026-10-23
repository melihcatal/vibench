import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def check_script_safety(script: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You review narration scripts for unsafe content and return strict JSON with keys safe, risk_level, issues, and rationale.",
            },
            {"role": "user", "content": script},
        ],
        "temperature": 0,
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python script_safety.py <script-file>")

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        script = f.read()

    result = check_script_safety(script)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
