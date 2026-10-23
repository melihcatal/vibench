import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claim(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

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

    result = (payload.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}

    flagged = bool(result.get("flagged"))
    highest_category = None
    highest_score = -1.0
    for category, score in category_scores.items():
        try:
            numeric_score = float(score)
        except (TypeError, ValueError):
            continue
        if numeric_score > highest_score:
            highest_score = numeric_score
            highest_category = category

    return {
        "flagged": flagged,
        "highest_category": highest_category,
        "highest_score": highest_score if highest_score >= 0 else None,
        "categories": categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "raw": payload,
    }


def moderate_claims(texts: List[str], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    if not isinstance(texts, list):
        raise ValueError("texts must be a list of strings")
    return [moderate_claim(text, api_key=api_key) for text in texts]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Moderate free-text claims or notes using OpenAI Moderation API")
    parser.add_argument("text", nargs="*", help="Text to moderate")
    args = parser.parse_args()

    if not args.text:
        raise SystemExit("Provide one or more text arguments")

    results = moderate_claims(args.text)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
