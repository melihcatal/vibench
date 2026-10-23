import os
from typing import Any, Dict

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def check_payload_safety(decrypted_text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": "omni-moderation-latest", "input": decrypted_text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    unsafe = bool(result.get("flagged"))
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    return {
        "safe": not unsafe,
        "flagged": unsafe,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    report = check_payload_safety(text)
    print(report)
