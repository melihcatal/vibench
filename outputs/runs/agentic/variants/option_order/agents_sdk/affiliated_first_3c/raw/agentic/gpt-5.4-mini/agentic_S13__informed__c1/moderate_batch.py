from __future__ import annotations

from typing import List

from safety_client import SafetyClient
from safety_models import BatchModerationResult, ModerationDecision, ModerationRequest, best_category, extract_category_scores, normalize_severity


def moderate_batch(requests: List[ModerationRequest]) -> BatchModerationResult:
    client = SafetyClient()
    texts = [req.text for req in requests]
    payload = client.analyze_batch(texts)
    items = payload.get("documents") or payload.get("items") or []
    decisions: List[ModerationDecision] = []
    for index, req in enumerate(requests):
        item = items[index] if index < len(items) and isinstance(items[index], dict) else {}
        scores = extract_category_scores(item)
        category = best_category(scores)
        severity = scores.get(category, normalize_severity(item.get("severity")))
        decisions.append(
            ModerationDecision(
                allow=severity < 0.5 and not bool(item.get("blocked", False)),
                category=category,
                severity=severity,
                rationale=item.get("rationale") or item.get("reason"),
                raw=item or {"text": req.text},
            )
        )
    return BatchModerationResult(decisions=decisions)
