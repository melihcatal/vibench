from typing import Iterable, List

from safety_client import AzureContentSafetyClient
from safety_models import SafetyBatchItem, SafetyModerationResult, normalize_score_map, normalize_text


def moderate_batch(items: Iterable[SafetyBatchItem]) -> List[SafetyModerationResult]:
    client = AzureContentSafetyClient()
    results: List[SafetyModerationResult] = []
    for item in items:
        payload = {"text": normalize_text(item.text)}
        raw = client.post("/contentsafety/text:analyze?api-version=2024-09-01", payload)
        categories = normalize_score_map(raw.get("categoriesAnalysis", {}))
        flagged = any(score >= 0.5 for score in categories.values()) or bool(raw.get("blocked", False))
        results.append(SafetyModerationResult(flagged=flagged, categories=categories, raw={"index": item.index, "user_id": item.user_id, **raw}))
    return results
