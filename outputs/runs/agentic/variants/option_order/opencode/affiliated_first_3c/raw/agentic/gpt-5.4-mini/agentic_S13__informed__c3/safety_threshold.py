from safety_client import SafetyClient
from safety_models import ThresholdRule, normalize_text


client = SafetyClient()


def safety_threshold(text: str, thresholds):
    payload = client.post("/text:analyze", {"text": normalize_text(text), "thresholds": [rule.__dict__ if isinstance(rule, ThresholdRule) else rule for rule in thresholds]})
    return payload.get("allowed", not payload.get("flagged", False))
