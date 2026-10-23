from openai import OpenAI

from safety_client import default_moderation_model, get_client, map_category_scores, moderation_thresholds
from safety_models import ThresholdResult, normalize_text


def safety_threshold(text: str) -> ThresholdResult:
    client: OpenAI = get_client()
    response = client.moderations.create(model=default_moderation_model(), input=normalize_text(text))
    result = response.results[0]
    scores = map_category_scores(getattr(result, "category_scores", None))
    thresholds = moderation_thresholds()
    triggered = [name for name, limit in thresholds.items() if scores.get(name, 0.0) >= limit]
    return ThresholdResult(allowed=not bool(triggered) and not bool(result.flagged), triggered=triggered, scores=scores)
