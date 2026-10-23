from typing import Dict, Any
from safety_models import ModerationResponse, ModerationRequest

def safety_threshold(moderation_response: ModerationResponse, thresholds: Dict[str, int]) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text.
    Returns a decision (allow/deny) and reasons based on the provided thresholds.
    """
    decision = "allow"
    reasons = []

    for category, severity in moderation_response.categories.items():
        if category in thresholds and severity >= thresholds[category]:
            decision = "deny"
            reasons.append(f"Category '{category}' with severity {severity} exceeded threshold {thresholds[category]}.")
    
    return {"decision": decision, "reasons": reasons, "severities": moderation_response.categories}

if __name__ == "__main__":
    # Example Usage
    # Assume a moderation response with severities for different categories
    mock_moderation_response = ModerationResponse(
        categories={
            "hate": 0,
            "self_harm": 2,
            "sexual": 4,
            "violence": 0,
        }
    )

    # Define thresholds for each category
    custom_thresholds = {
        "hate": 3,  # Deny if hate severity is 3 or more
        "self_harm": 3, # Deny if self_harm severity is 3 or more
        "sexual": 2, # Deny if sexual severity is 2 or more
        "violence": 3  # Deny if violence severity is 3 or more
    }

    decision_results = safety_threshold(mock_moderation_response, custom_thresholds)
    print(f"Decision for mock response: {decision_results}")

    mock_moderation_response_2 = ModerationResponse(
        categories={
            "hate": 0,
            "self_harm": 0,
            "sexual": 0,
            "violence": 5,
        }
    )
    decision_results_2 = safety_threshold(mock_moderation_response_2, custom_thresholds)
    print(f"Decision for second mock response: {decision_results_2}")
