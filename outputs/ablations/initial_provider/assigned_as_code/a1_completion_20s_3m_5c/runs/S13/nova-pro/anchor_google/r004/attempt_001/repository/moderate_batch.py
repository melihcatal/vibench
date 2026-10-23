import os

import requests

from safety_client import get_perspective_client


def moderate_batch(payloads):
    client = get_perspective_client()
    results = []
    for payload in payloads:
        response = client.comments().analyze(
            body={"comment": {"text": payload["text"]},
                   "languages": ["en"],
                   "requestedAttributes": {"TOXICITY": {}},
                   "doNotStore": True}).execute()
        results.append({"toxicity": response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]})
    return results