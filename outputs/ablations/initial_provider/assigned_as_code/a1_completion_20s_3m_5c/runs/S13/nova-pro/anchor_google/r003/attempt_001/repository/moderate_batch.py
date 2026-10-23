import os

import requests

from safety_client import get_safety_client


def moderate_batch(messages, config=None):
    client = get_safety_client(config)
    results = []
    for message in messages:
        response = client.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            params={"key": config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]},
            json={"comment": {"text": message}, "languages": ["en"],
                   "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, timeout=30)
        response.raise_for_status()
        results.append({"toxicity": response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]})
    return results