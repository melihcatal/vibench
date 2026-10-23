from typing import Dict, Any
from safety_models import ModerationResponse

def apply_safety_thresholds(moderation_response: ModerationResponse, thresholds: Dict[str, float]) -> Dict[str, Any]:
    decision = "ALLOW" # Default to allow
    reasons = []
    
    for category, severity in moderation_response.categories.items():
        # Azure Content Safety returns severity 0-7, normalize to 0-1 for threshold comparison
        normalized_severity = severity / 7.0
        
        if category in thresholds and normalized_severity > thresholds[category]:
            decision = "DENY"
            reasons.append(f"Category '{category}' exceeded threshold (severity: {normalized_severity:.2f}, threshold: {thresholds[category]:.2f})")
            
    if not reasons:
        reasons.append("No categories exceeded thresholds.")

    return {
        "text": moderation_response.text,
        "categories_severity": moderation_response.categories,
        "decision": decision,
        "reasons": reasons,
        "provider": "Azure Content Safety (implicit)" # Explicitly refer to the source of categories
    }
