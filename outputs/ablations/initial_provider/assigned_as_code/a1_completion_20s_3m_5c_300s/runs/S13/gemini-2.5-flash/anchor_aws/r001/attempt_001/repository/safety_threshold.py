from typing import Dict, Any, List
from safety_client import ComprehendSafetyClient
from safety_models import TextModerationRequest, ModerationDecision

def safety_threshold(text: str, thresholds: Dict[str, float], config: Dict[str, Any] = None) -> ModerationDecision:
    config = config or {}
    client = ComprehendSafetyClient(region_name=config.get("region", "us-east-1"))
    
    moderation_request = TextModerationRequest(text=text, language_code=config.get("language_code", "en"))
    moderation_response = client.detect_toxic_content(moderation_request)

    is_safe = True
    reasons = []
    scores = moderation_response.toxicity

    for category, threshold in thresholds.items():
        category_score = scores.get(category, {}).get("Score", 0.0)
        if category_score > threshold:
            is_safe = False
            reasons.append(f"Category '{category}' exceeded threshold with score {category_score:.2f} (threshold {threshold:.2f})")
    
    # If no specific category thresholds are provided or met, but overall is still unsafe per client's logic
    if not reasons and not moderation_response.content_safe:
        is_safe = False
        reasons.append("Content deemed unsafe by overall moderation policy")

    return ModerationDecision(text=text, is_safe=is_safe, reasons=reasons, scores=scores)
