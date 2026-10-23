from __future__ import annotations

from typing import Dict, List

from safety_client import hive_post
from safety_models import (
    SafetyCategoryScore,
    SafetyDecision,
    clamp_score,
    ensure_text,
    normalize_hive_class,
)


def moderate_text(text: str) -> SafetyDecision:
    content = ensure_text(text)
    payload = {"text_data": [{"text": content}]}
    data = hive_post(
        "/api/v2/task/sync", {"task": {"type": "text-moderation", "payload": payload}}
    )
    classes: List[Dict] = (
        data.get("status", [{}])[0]
        .get("response", {})
        .get("output", [{}])[0]
        .get("classes", [])
    )
    categories = []
    blocked = False
    for item in classes:
        score = clamp_score(item.get("score"))
        is_blocked = score >= 0.7
        blocked = blocked or is_blocked
        categories.append(
            SafetyCategoryScore(
                name=normalize_hive_class(item.get("class", "unknown")),
                score=score,
                blocked=is_blocked,
            )
        )
    return SafetyDecision(
        provider="Hive AI",
        allowed=not blocked,
        action="block" if blocked else "allow",
        categories=categories,
        raw=data,
    )
