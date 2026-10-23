from typing import Dict, Any, List
from safety_models import TextModerationResult, ModerationDecision

def safety_threshold(moderation_result: TextModerationResult, thresholds: Dict[str, float]) -> ModerationDecision:
    reasons = []
    allowed = True

    # Example: Apply thresholds based on category scores
    for category in moderation_result.categories:
        name = category["Name"]
        score = category["Score"]
        
        if name in thresholds and score > thresholds[name]:
            allowed = False
            reasons.append(f"Category '{name}' exceeded threshold with score {score:.2f} (threshold: {thresholds[name]:.2f})")
    
    # Apply overall toxicity threshold if present in scores
    if "Toxicity" in moderation_result.scores:
        toxicity_score = moderation_result.scores["Toxicity"]["Value"]
        if "overall_toxicity" in thresholds and toxicity_score > thresholds["overall_toxicity"]:
            allowed = False
            reasons.append(f"Overall toxicity exceeded threshold with score {toxicity_score:.2f} (threshold: {thresholds["overall_toxicity"]:.2f})")

    return ModerationDecision(
        text=moderation_result.text,
        allowed=allowed,
        reasons=reasons
    )
