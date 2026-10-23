import requests
from safety_client import build_safety_headers, load_safety_config
from safety_models import SafetyItem, normalize_text


THRESHOLDS = {"TOXICITY": 0.7, "INSULT": 0.6, "THREAT": 0.4, "SEVERE_TOXICITY": 0.3}


def safety_threshold(text: str) -> SafetyItem:
    config = load_safety_config()
    message = normalize_text(text)
    payload = {"comment": {"text": message}, "requestedAttributes": {name: {} for name in THRESHOLDS}}
    response = requests.post(f"{config.endpoint}/v1alpha1/comments:analyze", headers=build_safety_headers(config), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    categories = {k: data.get(k, {}).get("summaryScore", {}).get("value", 0.0) for k in THRESHOLDS}
    allow = all(categories[k] < threshold for k, threshold in THRESHOLDS.items())
    score = max(categories.values(), default=0.0)
    return SafetyItem(text=message, score=score, allow=allow, categories=categories)
