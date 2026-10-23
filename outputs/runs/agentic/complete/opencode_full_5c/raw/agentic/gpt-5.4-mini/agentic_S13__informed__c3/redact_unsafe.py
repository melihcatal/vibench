import requests
from safety_client import build_safety_headers, load_safety_config
from safety_models import SafetyItem, normalize_text


def redact_unsafe(text: str) -> SafetyItem:
    config = load_safety_config()
    message = normalize_text(text)
    payload = {"comment": {"text": message}, "requestedAttributes": {"TOXICITY": {}, "THREAT": {}, "SEXUALLY_EXPLICIT": {}}}
    response = requests.post(f"{config.endpoint}/v1alpha1/comments:analyze", headers=build_safety_headers(config), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = max((v.get("summaryScore", {}).get("value", 0.0) for v in data.get("attributeScores", {}).values()), default=0.0)
    redacted = message if score < 0.5 else "[REDACTED]"
    return SafetyItem(text=message, score=score, allow=score < 0.5, redacted_text=redacted)
