import json
import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _extract_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts: List[str] = []
        for item in value.values():
            text = _extract_text(item)
            if text:
                parts.append(text)
        return " ".join(parts)
    if isinstance(value, Iterable):
        parts = []
        for item in value:
            text = _extract_text(item)
            if text:
                parts.append(text)
        return " ".join(parts)
    return str(value)


def _collect_document_text(document: Dict[str, Any]) -> str:
    texts: List[str] = []
    for key, value in document.items():
        if isinstance(value, str):
            texts.append(value)
        elif isinstance(value, (dict, list, tuple, set)):
            nested = _extract_text(value)
            if nested:
                texts.append(nested)
    return "\n".join(texts)


def check_document_safety(document: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    text = _collect_document_text(document)
    if not text.strip():
        return {"safe": True, "reason": "no_text", "categories": {}, "category_scores": {}}

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

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
        "safe": not result.get("flagged", False),
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: record_text_safety.py '<json document>'")
    document = json.loads(sys.argv[1])
    result = check_document_safety(document)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
