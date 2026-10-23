from safety_client import moderate_text_request, threshold_value
from safety_models import ThresholdResult


def safety_threshold(text: str):
    decision = moderate_text_request(text)
    threshold = threshold_value()
    triggered = {k: v for k, v in decision.category_scores.items() if v >= threshold}
    return ThresholdResult(allowed=not bool(triggered), triggered=triggered, decision=decision)
