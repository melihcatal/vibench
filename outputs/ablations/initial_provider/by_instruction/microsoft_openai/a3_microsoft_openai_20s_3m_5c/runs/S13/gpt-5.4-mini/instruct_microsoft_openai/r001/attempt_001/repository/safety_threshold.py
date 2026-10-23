from safety_client import DEFAULT_MODERATION_MODEL, get_client, get_model
from safety_models import ThresholdResult, normalize_text


def safety_threshold(text, thresholds, model=None):
    value = normalize_text(text)
    client = get_client()
    moderation_model = get_model(model, DEFAULT_MODERATION_MODEL)
    response = client.moderations.create(model=moderation_model, input=value)
    result = response.results[0]
    triggered = []
    for category, threshold in (thresholds or {}).items():
        score = float((getattr(result, "category_scores", {}) or {}).get(category, 0.0))
        if score >= float(threshold):
            triggered.append(category)
    return ThresholdResult(allowed=not triggered and not bool(result.flagged), triggered=triggered, raw=response.model_dump())
