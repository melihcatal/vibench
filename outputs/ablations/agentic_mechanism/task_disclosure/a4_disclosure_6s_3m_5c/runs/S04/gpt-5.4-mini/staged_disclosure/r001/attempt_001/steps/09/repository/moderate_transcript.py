import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _chunks(text: str, max_chars: int = 4000) -> List[str]:
    if not text:
        return [""]
    parts: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        parts.append(text[start:end])
        start = end
    return parts


def moderate_text(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    findings: List[Dict[str, Any]] = []
    flagged = False

    for chunk in _chunks(text):
        response = requests.post(
            OPENAI_MODERATION_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"model": OPENAI_MODERATION_MODEL, "input": chunk},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        result = data["results"][0]
        flagged = flagged or bool(result.get("flagged"))
        findings.append(
            {
                "flagged": bool(result.get("flagged")),
                "categories": result.get("categories", {}),
                "category_scores": result.get("category_scores", {}),
            }
        )

    return {"flagged": flagged, "findings": findings, "text": text}


def main() -> None:
    input_text = sys.stdin.read()
    result = moderate_text(input_text)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
