import requests
from safety_client import build_safety_headers, load_safety_config
from safety_models import SafetyItem, normalize_text


def moderate_text(text: str) -> SafetyItem:
    config = load_safety_config()
    payload = {
        "comment": {"text": normalize_text(text)},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}}
    }
    response = requests.post(f"{config.endpoint}/v1alpha1/comments:analyze", headers=build_safety_headers(config), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    attrs = data.get("attributeScores", {})
    score = max((attrs.get(name, {}).get("summaryScore", {}).get("value", 0.0) for name in attrs), default=0.0)
    return SafetyItem(text=normalize_text(text), score=score, allow=score < 0.5, categories={k: v.get("summaryScore", {}).get("value", 0.0) for k, v in attrs.items()})
