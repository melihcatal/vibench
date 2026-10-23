from __future__ import annotations

from typing import Dict, Iterable, Optional

from safety_client import AzureContentSafetyClient
from safety_models import normalize_analysis_result


DEFAULT_THRESHOLDS = {
    "hate": 2,
    "selfharm": 1,
    "sexual": 2,
    "violence": 2,
}


def safety_threshold(
    text: str,
    thresholds: Optional[Dict[str, int]] = None,
    categories: Optional[Iterable[str]] = None,
) -> Dict[str, object]:
    client = AzureContentSafetyClient()
    response_json = client.analyze_text(text=text, categories=categories)
    result = normalize_analysis_result(text, response_json)
    effective = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    violations = []
    for category in result.categories:
        limit = effective.get(category.category, 4)
        sev = category.severity or 0
        if sev >= limit:
            violations.append({"category": category.category, "severity": sev, "threshold": limit})
    return {
        "provider": "azure-ai-content-safety",
        "allow": not violations and not result.blocklist_match,
        "violations": violations,
        "blocklist_match": result.blocklist_match,
        "raw_response": response_json,
    }
