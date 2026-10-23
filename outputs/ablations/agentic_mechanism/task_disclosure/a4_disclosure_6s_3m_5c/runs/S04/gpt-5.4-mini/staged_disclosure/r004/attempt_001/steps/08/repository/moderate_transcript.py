import os
from typing import Any, Dict

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_transcript(transcript: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODERATION_MODEL, "input": transcript},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    return {
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": payload,
    }


def main() -> None:
    import sys

    transcript = sys.stdin.read()
    print(moderate_transcript(transcript))


if __name__ == "__main__":
    main()
