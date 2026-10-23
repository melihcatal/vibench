import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_text(text: str) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    payload = {
        "model": OPENAI_MODEL,
        "input": text,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    if output:
        first = output[0]
        content = first.get("content", []) if isinstance(first, dict) else []
        if content:
            item = content[0]
            if isinstance(item, dict):
                return item.get("results", data)
    return data


def main() -> None:
    import sys

    text = sys.stdin.read()
    result = moderate_text(text)
    print(result)


if __name__ == "__main__":
    main()
