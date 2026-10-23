import os

import requests

from safety_models import normalize_batch_payload, extract_text_field


def moderate_batch(payload, config=None):
    config = config or {}
    data = normalize_batch_payload(payload)
    api_key = config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    decisions = []
    for item in data["messages"]:
        response = requests.post(url, params={"key": api_key}, json={"comment": {"text": extract_text_field(item)}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}}, "doNotStore": True}, timeout=30)
        response.raise_for_status()
        scores = response.json().get("attributeScores", {})
        decisions.append({"text": extract_text_field(item), "allow": float(scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)) < 0.5, "scores": scores})
    return {"decisions": decisions}
