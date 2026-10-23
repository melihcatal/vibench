import os

import requests

from safety_models import normalize_thresholds, parse_allowed_flag


def safety_threshold(payload, config=None):
    config = config or {}
    data = normalize_thresholds(payload)
    api_key = config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze", params={"key": api_key}, json={"comment": {"text": data["text"]}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}}, "doNotStore": True}, timeout=30)
    response.raise_for_status()
    scores = response.json().get("attributeScores", {})
    thresholds = data["thresholds"]
    categories = {}
    allow = True
    for category, score in scores.items():
        value = float(score.get("summaryScore", {}).get("value", 0.0))
        threshold = float(thresholds.get(category, 0.5))
        categories[category] = {"score": value, "threshold": threshold, "allow": parse_allowed_flag(value, threshold)}
        allow = allow and categories[category]["allow"]
    return {"allow": allow, "categories": categories}
