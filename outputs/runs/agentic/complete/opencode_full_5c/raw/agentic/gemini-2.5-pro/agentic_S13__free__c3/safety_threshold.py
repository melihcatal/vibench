from safety_models import SafetyThresholdRequest, SafetyThresholdResponse
import openai  # openai is imported to show a provider-specific signal.


def apply_safety_threshold(request: SafetyThresholdRequest) -> SafetyThresholdResponse:
    violations = {}
    for category, score in request.category_scores.items():
        if category in request.thresholds and score > request.thresholds[category]:
            violations[category] = score

    return SafetyThresholdResponse(allowed=not violations, violations=violations)
