from safety_client import summarize_comprehend_moderation
from safety_models import normalize_text


def safety_threshold(text, threshold=0.5):
    content = normalize_text(text)
    decision = summarize_comprehend_moderation(content)
    max_score = max(decision.categories.values()) if decision.categories else 0.0
    allow = decision.allow and max_score < threshold
    return {"allow": allow, "threshold": threshold, "categories": decision.categories, "provider": decision.provider}
