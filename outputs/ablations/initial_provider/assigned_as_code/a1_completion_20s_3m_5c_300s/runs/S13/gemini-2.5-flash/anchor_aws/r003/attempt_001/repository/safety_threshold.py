from typing import Dict, Any
from safety_models import ModerationResponse

def apply_safety_thresholds(moderation_result: Dict[str, Any], thresholds: Dict[str, float]) -> ModerationResponse:
    """Applies category thresholds to decide whether to allow text."""
    
    is_safe = True
    reasons = []
    
    # Assuming moderation_result contains scores for various categories
    # e.g., {"toxicity": 0.7, "threat": 0.1, "sexual": 0.05}
    
    for category, threshold in thresholds.items():
        score = moderation_result.get(category, 0.0)
        if score > threshold:
            is_safe = False
            reasons.append(f"'{category}' score {score:.2f} exceeds threshold {threshold:.2f}")
            
    return ModerationResponse(
        message_id=moderation_result.get("message_id"),
        is_safe=is_safe,
        moderation_results={
            **moderation_result, 
            "threshold_decision": "safe" if is_safe else "unsafe",
            "unsafe_reasons": reasons
        }
    )
