from typing import List, Dict, Any
from safety_models import ModerationResult

def safety_threshold(moderation_results: List[ModerationResult], thresholds: Dict[str, float]) -> Dict[str, Any]:
    decision = "ALLOW"
    reasons = []

    for result in moderation_results:
        category = result.category
        score = result.score
        threshold = thresholds.get(category, 1.0) # Default to 1.0 (no block) if threshold not specified

        if score >= threshold:
            decision = "DENY"
            reasons.append(f"{category} score ({score:.2f}) exceeds threshold ({threshold:.2f})")
            # For simplicity, we assume if one category exceeds, it's denied.
            # More complex logic could allow for partial denials or warnings.

    return {"overall_decision": decision, "reasons": reasons, "moderation_results": moderation_results}
