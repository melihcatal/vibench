from __future__ import annotations

from typing import Any, Dict, Iterable, List

from safety_client import ContentSafetyClient
from safety_models import ThresholdRule, parse_thresholds


def safety_threshold(text: str, thresholds: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = ContentSafetyClient()
    result = client.moderate_text(text)
    rules = parse_thresholds(thresholds)
    category = str(result.get("category", "unknown"))
    severity = float(result.get("severity", 0.0))
    matched = next((rule for rule in rules if rule.category == category), None)
    allowed = True if matched is None else severity <= matched.max_severity
    return {"allowed": allowed, "category": category, "severity": severity, "threshold": None if matched is None else matched.max_severity, "raw": result}
