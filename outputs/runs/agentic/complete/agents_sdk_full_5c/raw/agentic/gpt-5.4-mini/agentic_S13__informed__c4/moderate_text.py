from __future__ import annotations

from typing import Optional

from safety_client import AzureContentSafetyClient
from safety_models import ModerationDecision, SafetyModerationRequest, SafetyModerationResult, normalize_scores


def moderate_text(request: SafetyModerationRequest, client: Optional[AzureContentSafetyClient] = None) -> SafetyModerationResult:
    client = client or AzureContentSafetyClient()
    payload = client.analyze_text(request.text, request.categories)
    scores = normalize_scores(payload.get("categoriesAnalysis", {}))
    flags = {name: bool(value) for name, value in payload.get("categoriesFlags", {}).items()}
    flagged = bool(payload.get("isBlocked", False)) or any(flags.values())
    return SafetyModerationResult(
        flagged=flagged,
        category_scores=scores,
        category_flags=flags,
        provider_raw=payload,
        rationale=payload.get("reason"),
    )


def to_decision(result: SafetyModerationResult) -> ModerationDecision:
    return ModerationDecision(
        allowed=not result.flagged,
        flagged=result.flagged,
        reason=result.rationale or ("blocked" if result.flagged else "allowed"),
        scores=result.category_scores,
    )
