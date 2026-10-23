from __future__ import annotations

from typing import Any

from safety_client import analyze_text
from safety_models import SafetyRequest


REDACTION_TOKEN = "[UNSAFE]"


def redact_unsafe(text: str, threshold: float = 2.0) -> dict[str, Any]:
    result = analyze_text(SafetyRequest(text=text))
    max_score = max(result.categories.values(), default=0.0)
    redacted_text = REDACTION_TOKEN if max_score >= threshold else text
    return {
        "provider": "azure-ai-content-safety",
        "text": text,
        "redacted_text": redacted_text,
        "flagged": result.flagged,
        "categories": result.categories,
    }
