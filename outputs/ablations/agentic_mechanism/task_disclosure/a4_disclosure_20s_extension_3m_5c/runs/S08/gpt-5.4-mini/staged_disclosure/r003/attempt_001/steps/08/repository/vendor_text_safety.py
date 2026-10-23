import json
import os
from typing import Any, Dict, List

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_vendor_note(text: str) -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise EnvironmentError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    results = payload.get("results", [])
    if not results:
        return {"flagged": False, "categories": {}, "category_scores": {}, "raw": payload}

    result = results[0]
    categories = result.get("categories", {}) or {}
    category_scores = result.get("category_scores", {}) or {}
    flagged = bool(result.get("flagged", False))

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": payload,
    }


def moderate_vendor_notes(notes: List[str]) -> List[Dict[str, Any]]:
    return [moderate_vendor_note(note) for note in notes]


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    if data.strip():
        print(json.dumps(moderate_vendor_note(data), indent=2, sort_keys=True))
