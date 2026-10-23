import os

import requests

from safety_client import get_perspective_client


def redact_unsafe(payload):
    client = get_perspective_client()
    response = client.comments().analyze(
        body={"comment": {"text": payload["text"]},
               "languages": ["en"],
               "requestedAttributes": {"TOXICITY": {}},
               "doNotStore": True}).execute()
    toxicity = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    if toxicity > 0.5:
        return "[REDACTED]"
    return payload["text"]