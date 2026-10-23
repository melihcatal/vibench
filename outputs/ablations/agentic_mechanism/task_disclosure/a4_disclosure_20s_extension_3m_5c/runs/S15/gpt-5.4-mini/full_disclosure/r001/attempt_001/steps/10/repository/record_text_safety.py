import os
from typing import Any, Dict, List, Optional

import requests


def _get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def _extract_text_fields(record: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key, value in record.items():
        if isinstance(value, str):
            parts.append(f"{key}: {value}")
        elif isinstance(value, dict):
            nested = _extract_text_fields(value)
            if nested:
                parts.append(f"{key}: {nested}")
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    parts.append(f"{key}: {item}")
                elif isinstance(item, dict):
                    nested = _extract_text_fields(item)
                    if nested:
                        parts.append(f"{key}: {nested}")
    return "\n".join(parts)


def record_text_safety(record: Dict[str, Any], model: str = "omni-moderation-latest") -> Dict[str, Any]:
    text = _extract_text_fields(record)
    if not text.strip():
        return {"safe": True, "categories": {}, "category_scores": {}, "flagged": False, "provider": "openai"}

    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return {
        "safe": not result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "flagged": result.get("flagged", False),
        "provider": "openai",
        "model": model,
    }
