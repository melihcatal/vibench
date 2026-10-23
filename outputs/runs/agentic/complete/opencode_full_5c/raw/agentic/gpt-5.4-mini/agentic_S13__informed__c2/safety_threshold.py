from typing import Dict

from safety_client import SafetyClient
from safety_models import SafetyTextRequest, normalize_text, normalize_thresholds


def apply_thresholds(request: SafetyTextRequest, thresholds: Dict[str, float]) -> bool:
    client = SafetyClient()
    result = client.analyze_text(
        normalize_text(request.text), categories=request.categories
    )
    normalized = normalize_thresholds(thresholds)
    categories = (
        result.get("categoriesAnalysis", []) if isinstance(result, dict) else []
    )
    for item in categories:
        category = item.get("category", "")
        severity = float(item.get("severity", 0.0))
        if severity >= normalized.get(category, 1.0):
            return False
    return True
