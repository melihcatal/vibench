import os
import requests

def moderate_batch(payloads, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]
    results = []
    for payload in payloads:
        response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            params={"key": api_key},
            json={"comment": {"text": payload["text"]}, "languages": ["en"],
                  "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, timeout=30)
        response.raise_for_status()
        results.append({"text": payload["text"], "toxicity": response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]})
    return results
