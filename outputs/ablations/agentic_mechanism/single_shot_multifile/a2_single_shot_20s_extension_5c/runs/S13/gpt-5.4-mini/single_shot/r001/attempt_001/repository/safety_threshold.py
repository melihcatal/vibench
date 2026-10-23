from typing import Any, Dict
from safety_client import get_openai_client, get_moderation_model_name, get_category_thresholds
from safety_models import normalize_text_input, build_threshold_decision


def safety_threshold(text: str, *, thresholds: Dict[str, float] | None = None, model: str | None = None) -> Dict[str, Any]:
    client = get_openai_client()
    payload = normalize_text_input(text)
    model_name = model or get_moderation_model_name()
    configured_thresholds = thresholds or get_category_thresholds()
    response = client.moderations.create(model=model_name, input=payload["text"])
    result = response.results[0]
    categories = dict(result.category_scores)
    allow = True
    triggered = {}
    for category, score in categories.items():
        threshold = configured_thresholds.get(category, 1.0)
        hit = score >= threshold
        triggered[category] = {"score": score, "threshold": threshold, "hit": hit}
        if hit:
            allow = False
    return build_threshold_decision(text=payload["text"], allow=allow, triggered=triggered, model=model_name)


if __name__ == "__main__":
    raise SystemExit(0)
