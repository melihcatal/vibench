from safety_client import get_openai_client, moderation_model, parse_moderation_result
from safety_models import SafetyThresholds, TextSafetyRequest


def safety_threshold(value, thresholds=None):
    req = TextSafetyRequest.from_input(value)
    th = SafetyThresholds.from_input(thresholds)
    client = get_openai_client()
    result = client.moderations.create(model=moderation_model(), input=req.text)
    parsed = parse_moderation_result(result)
    item = parsed.get("results", [{}])[0]
    scores = item.get("category_scores", {})
    allowed = not any(
        scores.get(k, 0.0) >= getattr(th, k, 1.0)
        for k in ["violence", "self_harm", "sexual", "hate", "harassment"]
    )
    return {
        "allowed": allowed,
        "scores": scores,
        "thresholds": th.__dict__,
        "raw": parsed,
    }
