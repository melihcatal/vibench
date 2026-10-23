import os
from typing import Dict, Any

# Assuming safety_models.py defines a structure like this for moderation results
# For demonstration, we'll use a dictionary.
# from safety_models import ModerationResult

def apply_safety_thresholds(
    moderation_output: Dict[str, Any],
    thresholds: Dict[str, float],
    default_allow: bool = True
) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text based on moderation results.
    This function expects moderation_output to be in a normalized format,
    potentially from a helper like safety_models.py.

    Args:
        moderation_output: A dictionary containing moderation results.
                           Expected format: {"category_name": {"score": float}}
                           or from Azure: {"category_name": {"violated": bool, "severity": int}}
        thresholds: A dictionary mapping category names to their maximum allowed score (for score-based systems)
                    or minimum severity (for severity-based systems to be flagged).
                    e.g., {"Hate": 0.5, "SelfHarm": 0.8} for scores, or {"Sexual": 2, "Violence": 3} for Azure severity.
        default_allow: If True, text is allowed if no explicit violation is found or thresholds are not met.

    Returns:
        A dictionary indicating the decision and reasons.
    """
    
    decision = "ALLOW" if default_allow else "DENY"
    reasons = []

    # Example for Google Cloud Natural Language API-like output (confidence scores)
    if "moderation_results" in moderation_output and isinstance(moderation_output["moderation_results"], list):
        for result in moderation_output["moderation_results"]:
            category = result.get("category")
            confidence = result.get("confidence")
            if category and confidence is not None:
                if category in thresholds and confidence > thresholds[category]:
                    decision = "DENY"
                    reasons.append(f"Category '{category}' confidence ({confidence:.2f}) exceeds threshold ({thresholds[category]:.2f})")

    # Example for Azure Content Safety API-like output (severity and violated flags)
    elif "moderation_results" in moderation_output and isinstance(moderation_output["moderation_results"], dict):
        for category, data in moderation_output["moderation_results"].items():
            violated = data.get("violated")
            severity = data.get("severity")
            
            if violated is True: # If the service already marked it as violated
                if category in thresholds: # Check against custom severity threshold if provided
                    if severity is not None and severity >= thresholds[category]:
                        decision = "DENY"
                        reasons.append(f"Category '{category}' violated with severity ({severity}) at or above threshold ({thresholds[category]})")
                else: # If violated but no specific severity threshold, just flag it as violated
                    decision = "DENY"
                    reasons.append(f"Category '{category}' explicitly violated by service.")
            elif severity is not None and category in thresholds and severity >= thresholds[category]:
                 # If not explicitly violated by service, but severity is above custom threshold
                 decision = "DENY"
                 reasons.append(f"Category '{category}' severity ({severity}) exceeds threshold ({thresholds[category]})")


    return {
        "decision": decision,
        "reasons": reasons if reasons else ["No violations found or thresholds not met."]
    }

if __name__ == '__main__':
    # Example 1: Google Cloud Natural Language-like output
    gcp_moderation_output = {
        "moderation_results": [
            {"category": "Hate speech", "confidence": 0.9},
            {"category": "Violence", "confidence": 0.3},
            {"category": "Sexual content", "confidence": 0.1}
        ]
    }
    gcp_thresholds = {
        "Hate speech": 0.7,  # High threshold
        "Violence": 0.5     # Moderate threshold
    }
    gcp_decision = apply_safety_thresholds(gcp_moderation_output, gcp_thresholds)
    print(f"GCP-like decision: {gcp_decision['decision']}, Reasons: {gcp_decision['reasons']}")

    # Example 2: Azure Content Safety-like output
    azure_moderation_output = {
        "moderation_results": {
            "Hate": {"violated": True, "severity": 4},
            "Sexual": {"violated": False, "severity": 1},
            "Violence": {"violated": True, "severity": 2}
        }
    }
    azure_thresholds = {
        "Hate": 2,     # If severity is 2 or higher, flag
        "Violence": 3  # If severity is 3 or higher, flag
    }
    azure_decision = apply_safety_thresholds(azure_moderation_output, azure_thresholds)
    print(f"\nAzure-like decision: {azure_decision['decision']}, Reasons: {azure_decision['reasons']}")

    # Example 3: Allowed text
    safe_moderation_output = {
        "moderation_results": [
            {"category": "Harassment", "confidence": 0.1},
            {"category": "Threat", "confidence": 0.05}
        ]
    }
    safe_thresholds = {
        "Harassment": 0.6,
        "Threat": 0.7
    }
    safe_decision = apply_safety_thresholds(safe_moderation_output, safe_thresholds)
    print(f"\nSafe text decision: {safe_decision['decision']}, Reasons: {safe_decision['reasons']}")
