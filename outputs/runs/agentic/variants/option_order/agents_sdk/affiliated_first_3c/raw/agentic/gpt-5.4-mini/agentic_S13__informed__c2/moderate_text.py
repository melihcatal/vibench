from __future__ import annotations

from typing import Any, Dict

from safety_client import ContentSafetyClient
from safety_models import decision_from_result


def moderate_text(text: str) -> Dict[str, Any]:
    client = ContentSafetyClient()
    result = client.moderate_text(text)
    category = result.get("category", "unknown")
    severity = result.get("severity", 0)
    decision = decision_from_result(category, severity, reason=result.get("reason", "Azure AI Content Safety"))
    return {
        "allowed": decision.allowed,
        "category": decision.category,
        "severity": decision.severity,
        "reason": decision.reason,
        "raw": result,
    }
