import os
import json
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
OPENAI_API_URL = "https://api.openai.com/v1/moderations"


def check_live_caption_safety(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    unsafe_categories = [name for name, value in categories.items() if value]
    return {
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "raw": data,
    }


def is_safe(text: str, api_key: Optional[str] = None) -> bool:
    return not check_live_caption_safety(text, api_key=api_key)["flagged"]


def main() -> None:
    import sys

    text = sys.stdin.read()
    result = check_live_caption_safety(text)
    sys.stdout.write(json.dumps(result))


if __name__ == "__main__":
    main()
