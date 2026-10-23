import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_claim(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    return {
        "flagged": bool(result.get("flagged")),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": payload,
    }


def moderate_claims(texts: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    if isinstance(texts, str):
        texts = [texts]
    findings = [moderate_claim(text, api_key=api_key) for text in texts]
    return {"results": findings, "any_flagged": any(item["flagged"] for item in findings)}


if __name__ == "__main__":
    import sys

    input_text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()
    print(json.dumps(moderate_claim(input_text), ensure_ascii=False))
