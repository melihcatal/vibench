import os

import requests

from safety_client import get_perspective_client


def appeal_translate(text, target_language='es'):
    client = get_perspective_client()
    response = client.comments().analyze(
        body={"comment": {"text": text},
               "languages": ["en"],
               "requestedAttributes": {"TOXICITY": {}},
               "doNotStore": True}).execute()
    toxicity = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    if toxicity > 0.5:
        return f"[Translation of appeal text in {target_language}]" + text
    return text