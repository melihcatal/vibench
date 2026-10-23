from __future__ import annotations

from typing import Any, Dict, List

from database_models import SafetyResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_text_safety(record: Dict[str, Any]) -> SafetyResult:
    text = " ".join(str(record.get(k, "")) for k in ("title", "description", "content", "body"))
    reasons: List[str] = []
    unsafe_terms = ["hate", "violence", "self-harm", "explosive", "weapon"]
    lowered = text.lower()
    for term in unsafe_terms:
        if term in lowered:
            reasons.append(term)
    return SafetyResult(document_id=str(record.get("document_id", "")), is_safe=not reasons, reasons=reasons)
