import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _read_input() -> str:
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def _build_prompt(script: str) -> str:
    return (
        "Check the following narration script for unsafe content. "
        "Return strict JSON with keys: unsafe (boolean), reasons (array of strings), "
        "categories (array of strings), and summary (string).\n\n"
        f"SCRIPT:\n{script}"
    )


def analyze_script(script: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [{"type": "text", "text": _build_prompt(script)}],
            }
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


def main() -> None:
    script = _read_input()
    result = analyze_script(script)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
