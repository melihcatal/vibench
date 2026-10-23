import os
import requests

def redact_unsafe(payload, config=None, threshold=0.7):
    config = config or {}
    api_key = config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]
    
    response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={"comment": {"text": payload["text"]}, "languages": ["en"],
              "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, timeout=30)
    response.raise_for_status()
    
    toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    
    if toxicity_score > threshold:
        return {"original_text": payload["text"], "redacted_text": "[REDACTED]", "toxicity": toxicity_score, "is_unsafe": True}
    else:
        return {"original_text": payload["text"], "redacted_text": payload["text"], "toxicity": toxicity_score, "is_unsafe": False}
