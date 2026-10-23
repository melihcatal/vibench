# safety_threshold.py
import os

def apply_thresholds(moderation_results: dict, thresholds: dict) -> dict:
    """Applies per-category thresholds to moderation results and returns a consolidated decision.
    moderation_results should be a dict with category -> score (e.g. {'hate': 0.73, ...})
    Returns a dict: {'overall_decision': 'allow'|'block', 'details': {...}}"""
    decision = "allow"
    details = {}
    for cat, min_score in thresholds.items():
        score = moderation_results.get(cat, 0.0)
        details[cat] = {
            "score": score,
            "threshold": min_score
        }
        if score >= min_score:
            # If any category exceeds its threshold, block the content
            decision = "block"
    return {
        "decision": decision,
        "category_details": details
    }

if __name__ == "__main__":
    # Example usage
    moderation = {
        "hate": 0.81,
        "self_harm": 0.48,
        "sexual": 0.0,
        "violence": 0.92
    }
    thresholds = {
        "hate": 0.7,
        "self_harm": 0.5,
        "sexual": 0.0,
        "violence": 0.7
    }
    print(apply_thresholds(moderation, thresholds))