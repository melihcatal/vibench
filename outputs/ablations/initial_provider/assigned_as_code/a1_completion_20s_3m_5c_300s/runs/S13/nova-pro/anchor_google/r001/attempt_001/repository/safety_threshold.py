import os

import requests

from safety_client import get_client


def safety_threshold(text, threshold=0.5, config=None):
    client = get_client(config)
    response = client.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": text}, "languages": ["en"],
               "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, timeout=30)
    response.raise_for_status()
    toxicity = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity <= threshold