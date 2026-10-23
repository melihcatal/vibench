from safety_client import get_client, model_name
from safety_models import normalize_text


def safety_threshold(text: str, thresholds):
    client = get_client()
    response = client.moderations.create(
        model=model_name("omni-moderation-latest"), input=normalize_text(text)
    )
    result = response.results[0]
    scores = dict(getattr(result, "category_scores", {}) or {})
    for category, threshold in (thresholds or {}).items():
        if scores.get(category, 0.0) >= threshold:
            return False
    return not bool(getattr(result, "flagged", False))
