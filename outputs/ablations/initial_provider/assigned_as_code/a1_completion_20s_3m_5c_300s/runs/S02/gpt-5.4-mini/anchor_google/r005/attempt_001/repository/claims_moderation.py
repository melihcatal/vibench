import requests


def claims_moderation(payload, config=None):
    config = dict(config or {})
    response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                             params={"key": config["api_key"]}, json={"comment": {"text": payload["text"]}, "requestedAttributes": {"TOXICITY": {}}}, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"text": payload["text"], "toxicity": result.get("attributeScores", {}).get("TOXICITY", {})}
