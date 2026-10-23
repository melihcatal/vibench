import os

import requests

from safety_client import get_perspective_client


def moderation_reason_embedding(reason):
    client = get_perspective_client()
    response = client.comments().analyze(
        body={"comment": {"text": reason},
               "languages": ["en"],
               "requestedAttributes": {"TOXICITY": {}},
               "doNotStore": True}).execute()
    toxicity = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"reason": reason, "toxicity": toxicity}