import json
import os
from typing import Any, Dict, List, Optional

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
    if isinstance(value, list):
        parts = []
        for item in value:
            text = _extract_text(item)
            if text:
                parts.append(text)
        return " ".join(parts)
    return str(value)


def _scan_fields(document: Dict[str, Any], fields: Optional[List[str]] = None) -> Dict[str, str]:
    if fields:
        return {field: _extract_text(document.get(field, "")) for field in fields}
    return {key: _extract_text(value) for key, value in document.items()}


def _moderate_text(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
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
    return response.json()


def check_record_text_safety(document: Dict[str, Any], fields: Optional[List[str]] = None) -> Dict[str, Any]:
    scanned_fields = _scan_fields(document, fields)
    results: Dict[str, Any] = {}
    unsafe: Dict[str, Any] = {}
    for field, text in scanned_fields.items():
        if not text.strip():
            results[field] = {"safe": True, "categories": {}, "flagged": False}
            continue
        moderation = _moderate_text(text)
        item = moderation["results"][0]
        field_result = {
            "safe": not item.get("flagged", False),
            "flagged": item.get("flagged", False),
            "categories": item.get("categories", {}),
            "category_scores": item.get("category_scores", {}),
        }
        results[field] = field_result
        if field_result["flagged"]:
            unsafe[field] = field_result
    return {"safe": not unsafe, "fields": results, "unsafe_fields": unsafe}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("document", help="JSON document string")
    parser.add_argument("--fields", nargs="*")
    args = parser.parse_args()
    document = json.loads(args.document)
    print(json.dumps(check_record_text_safety(document, args.fields), ensure_ascii=False))


if __name__ == "__main__":
    main()
