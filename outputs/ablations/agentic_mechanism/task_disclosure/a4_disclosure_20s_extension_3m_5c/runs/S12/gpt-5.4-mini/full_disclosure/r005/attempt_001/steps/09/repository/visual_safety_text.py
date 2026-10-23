import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _normalize_labels(labels: Any) -> str:
    if labels is None:
        return ""
    if isinstance(labels, str):
        return labels.strip()
    if isinstance(labels, dict):
        parts = []
        for key, value in labels.items():
            if value is None:
                continue
            parts.append(f"{key}: {value}")
        return "\n".join(parts)
    if isinstance(labels, (list, tuple, set)):
        return "\n".join(str(item).strip() for item in labels if str(item).strip())
    return str(labels).strip()


def check_generated_visual_labels_for_unsafe_text(labels: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    text = _normalize_labels(labels)
    if not text:
        return {"unsafe": False, "categories": {}, "category_scores": {}, "flagged": False, "input": text}

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {"model": OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data.get("results", [{}])[0]
    categories = result.get("categories", {}) or {}
    category_scores = result.get("category_scores", {}) or {}
    flagged = bool(result.get("flagged", False))
    return {
        "unsafe": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "flagged": flagged,
        "input": text,
    }


def main() -> None:
    import sys

    labels = sys.stdin.read()
    result = check_generated_visual_labels_for_unsafe_text(labels)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
