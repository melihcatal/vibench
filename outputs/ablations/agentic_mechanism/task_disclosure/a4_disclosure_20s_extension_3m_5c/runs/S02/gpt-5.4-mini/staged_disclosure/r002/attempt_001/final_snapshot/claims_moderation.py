import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claim(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
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


def moderate_claims(notes: List[str], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    return [moderate_claim(note, api_key=api_key) for note in notes]


def main() -> None:
    import sys

    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("Provide free-text claims or notes via stdin")
    print(json.dumps(moderate_claim(text), ensure_ascii=False))


if __name__ == "__main__":
    main()
