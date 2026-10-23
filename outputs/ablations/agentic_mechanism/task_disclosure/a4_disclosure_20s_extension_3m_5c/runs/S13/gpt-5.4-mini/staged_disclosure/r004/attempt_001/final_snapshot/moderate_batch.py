import json
import os
from typing import List, Dict, Any

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"input": messages},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    results = payload.get("results", [])
    decisions: List[Dict[str, Any]] = []
    for message, result in zip(messages, results):
        categories = result.get("categories", {})
        flagged = bool(result.get("flagged", False))
        decisions.append(
            {
                "message": message,
                "decision": "block" if flagged else "allow",
                "flagged": flagged,
                "categories": categories,
            }
        )
    return decisions


def main() -> None:
    import sys

    messages = json.loads(sys.stdin.read() or "[]")
    if not isinstance(messages, list) or not all(isinstance(item, str) for item in messages):
        raise ValueError("Input must be a JSON array of strings")
    print(json.dumps(moderate_batch(messages)))


if __name__ == "__main__":
    main()
