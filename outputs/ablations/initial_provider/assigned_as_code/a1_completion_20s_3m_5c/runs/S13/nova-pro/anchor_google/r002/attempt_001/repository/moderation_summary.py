import os

import requests


def moderation_summary(payloads, config=None):
    summary = {}
    for payload in payloads:
        response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            params={"key": config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]},
            json={"comment": {"text": payload["text"]}, "languages": ["en"],
                   "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, timeout=30)
        response.raise_for_status()
        toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        summary[payload["text"]] = toxicity_score
    return summary