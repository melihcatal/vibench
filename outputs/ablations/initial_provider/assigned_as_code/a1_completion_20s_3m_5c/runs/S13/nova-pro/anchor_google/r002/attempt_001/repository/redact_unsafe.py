import os

import requests

from safety_client import get_safety_client


def redact_unsafe(payload, config=None):
    client = get_safety_client(config)
    response = client.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": payload["text"]}, "languages": ["en"],
               "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, timeout=30)
    response.raise_for_status()
    toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    if toxicity_score > 0.5:
        return "**REDACTED**"
    else:
        return payload["text"]