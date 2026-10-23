import json
import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_profile_text(profile_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": profile_text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    flagged_categories: List[str] = [name for name, flagged in categories.items() if flagged]

    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "flagged": bool(result.get("flagged", False)),
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
        "raw": result,
    }


def should_activate_account(profile_text: str) -> bool:
    moderation = moderate_profile_text(profile_text)
    return not moderation["flagged"]


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: profile_moderation.py <profile_text>")

    profile_text = " ".join(sys.argv[1:]).strip()
    result = moderate_profile_text(profile_text)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
