from safety_client import prepare_text_payload, post_perspective
from safety_models import ModerationDecision, normalize_score, normalize_text


def safety_threshold(text, thresholds=None, language=None):
    thresholds = thresholds or {"TOXICITY": 0.5}
    original = normalize_text(text)
    raw = post_perspective(prepare_text_payload(original, language))
    categories = {}
    allow = True
    for category, threshold in thresholds.items():
        score = normalize_score(
            raw.get("attributeScores", {})
            .get(category, {})
            .get("summaryScore", {})
            .get("value")
        )
        categories[category] = score
        if score >= threshold:
            allow = False
    return ModerationDecision(
        allow=allow,
        score=max(categories.values()) if categories else 0.0,
        categories=categories,
        raw=raw,
    )
