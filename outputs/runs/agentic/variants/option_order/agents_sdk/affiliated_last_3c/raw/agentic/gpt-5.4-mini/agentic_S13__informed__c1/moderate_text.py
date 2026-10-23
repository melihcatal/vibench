from __future__ import annotations

from typing import Dict, List

from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import SafetyClient
from safety_models import SafetyCategoryScore, SafetyModerationDecision, SafetyModerationRequest, clamp_score


def moderate_text(request: SafetyModerationRequest) -> SafetyModerationDecision:
    client = SafetyClient()
    text = client.normalize(request.text)
    if client.client is not None:
        result = client.client.analyze_text(AnalyzeTextOptions(text=text))
        category_scores: List[SafetyCategoryScore] = []
        for item in getattr(result, "categories_analysis", []):
            category_scores.append(
                SafetyCategoryScore(
                    category=getattr(item, "category", "unknown"),
                    score=clamp_score(getattr(item, "severity", 0) / 7.0),
                )
            )
        flagged = any(score.is_flagged() for score in category_scores)
        return SafetyModerationDecision(flagged=flagged, category_scores=category_scores, provider="azure-ai-content-safety", raw={"text": text})
    payload: Dict[str, object] = {"text": text, "categories": list(request.categories)}
    raw = client.post(payload)
    scores = raw.get("categoriesAnalysis", {}) if isinstance(raw, dict) else {}
    decision = SafetyModerationDecision(flagged=False, provider="azure-ai-content-safety", raw=raw if isinstance(raw, dict) else {})
    decision.category_scores = [SafetyCategoryScore(category=k, score=clamp_score(v)) for k, v in scores.items()]
    decision.flagged = any(s.is_flagged() for s in decision.category_scores)
    return decision
