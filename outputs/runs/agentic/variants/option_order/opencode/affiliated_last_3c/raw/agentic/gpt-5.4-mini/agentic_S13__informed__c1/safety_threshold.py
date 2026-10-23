from safety_client import SafetyClient
from safety_models import (
    SafetyDecision,
    ThresholdRule,
    coerce_thresholds,
    normalize_language,
    normalize_text,
)


def safety_threshold(text, thresholds, language=None):
    client = SafetyClient()
    rules = [
        ThresholdRule(category=k, threshold=v)
        for k, v in coerce_thresholds(thresholds).items()
    ]
    payload = {"text": normalize_text(text)}
    lang = normalize_language(language)
    if lang:
        payload["language"] = lang
    data = client.post("/contentsafety/text:analyze?api-version=2024-09-01", payload)
    categories = {
        item.get("category", "unknown"): float(item.get("severity", 0))
        for item in data.get("categoriesAnalysis", [])
    }
    allowed = True
    for rule in rules:
        if categories.get(rule.category, 0.0) >= rule.threshold:
            allowed = False
    return SafetyDecision(allowed=allowed, categories=categories, raw=data)
