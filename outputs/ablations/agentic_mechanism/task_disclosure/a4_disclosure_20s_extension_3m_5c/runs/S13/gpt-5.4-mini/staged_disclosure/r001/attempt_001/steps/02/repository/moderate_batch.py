import json
import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    api_key = os.environ["OPENAI_API_KEY"]
    payload = {
        "model": OPENAI_MODEL,
        "input": messages,
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
    if not output:
        return []
    content = output[0].get("content", []) if isinstance(output[0], dict) else []
    if not content:
        return []
    item = content[0]
    if isinstance(item, dict):
        results = item.get("results", [])
        if isinstance(results, list):
            return results
    return []


def main() -> None:
    import sys

    messages = json.loads(sys.stdin.read() or "[]")
    print(json.dumps(moderate_batch(messages)))


if __name__ == "__main__":
    main()
