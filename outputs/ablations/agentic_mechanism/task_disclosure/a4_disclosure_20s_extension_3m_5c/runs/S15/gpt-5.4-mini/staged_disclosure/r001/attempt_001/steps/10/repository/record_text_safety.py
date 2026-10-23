import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def _collect_text_fields(record: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for key, value in record.items():
        if isinstance(value, str):
            texts.append(value)
        elif isinstance(value, dict):
            texts.extend(_collect_text_fields(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    texts.append(item)
                elif isinstance(item, dict):
                    texts.extend(_collect_text_fields(item))
    return texts


def _moderate_text(text: str, api_key: str, timeout: float = 30.0) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": text},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    categories = result.get("categories", {})
    scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    unsafe_categories = [name for name, is_flagged in categories.items() if is_flagged]
    return {
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "scores": scores,
        "raw": result,
    }


def record_text_safety(record: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    texts = _collect_text_fields(record)
    findings: List[Dict[str, Any]] = []
    unsafe = False

    for text in texts:
        moderation = _moderate_text(text, api_key)
        findings.append({"text": text, **moderation})
        if moderation["flagged"]:
            unsafe = True

    return {"safe": not unsafe, "findings": findings}


def is_record_safe(record: Dict[str, Any], api_key: Optional[str] = None) -> bool:
    return bool(record_text_safety(record, api_key)["safe"])
