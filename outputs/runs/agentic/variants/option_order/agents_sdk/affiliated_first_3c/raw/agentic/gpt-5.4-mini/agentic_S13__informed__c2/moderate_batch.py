from __future__ import annotations

from typing import Any, Dict, List

from safety_client import ContentSafetyClient
from safety_models import decision_from_result


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    client = ContentSafetyClient()
    results = []
    for message in messages:
        result = client.moderate_text(message)
        category = result.get("category", "unknown")
        severity = result.get("severity", 0)
        decision = decision_from_result(category, severity, reason=result.get("reason", "Azure AI Content Safety"))
        results.append({"message": message, "allowed": decision.allowed, "category": decision.category, "severity": decision.severity})
    return results
