import requests
from safety_client import build_safety_headers, load_safety_config
from safety_models import SafetyItem, normalize_batch


def moderate_batch(messages):
    config = load_safety_config()
    outputs = []
    for message in normalize_batch(messages):
        payload = {"comment": {"text": message}, "requestedAttributes": {"TOXICITY": {}, "INSULT": {}}}
        response = requests.post(f"{config.endpoint}/v1alpha1/comments:analyze", headers=build_safety_headers(config), json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        score = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
        outputs.append(SafetyItem(text=message, score=score, allow=score < 0.5, categories={"TOXICITY": score}))
    return outputs
