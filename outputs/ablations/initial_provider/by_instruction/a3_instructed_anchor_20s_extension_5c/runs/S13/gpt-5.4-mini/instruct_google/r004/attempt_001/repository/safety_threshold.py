from safety_models import SafetyDecision


def safety_threshold(decision: SafetyDecision, thresholds: dict) -> bool:
    for category, threshold in thresholds.items():
        if decision.category_scores.get(category, 0.0) >= threshold:
            return False
    return decision.allowed
