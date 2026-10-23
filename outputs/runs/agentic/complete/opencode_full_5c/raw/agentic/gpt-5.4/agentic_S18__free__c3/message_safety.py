from __future__ import annotations

from typing import Any, Dict

from messaging_client import MODERATE_API_BASE, openai_headers, post_json
from messaging_models import ensure_text


def message_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = ensure_text(payload.get("text") or payload.get("message") or payload)
    response = post_json(
        f"{MODERATE_API_BASE}/moderations",
        {
            "model": "omni-moderation-latest",
            "input": text,
        },
        openai_headers(),
    )
    result = response.get("results", [{}])[0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
    }
