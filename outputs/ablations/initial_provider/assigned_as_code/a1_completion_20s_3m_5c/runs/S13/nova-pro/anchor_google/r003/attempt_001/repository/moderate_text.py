import os

import requests


def moderate_text(payload, config=None):
    config = config or {}
    response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": payload["text"]}, "languages": ["en"],
              "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, timeout=30)
    response.raise_for_status()
    return {"toxicity": response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]}
