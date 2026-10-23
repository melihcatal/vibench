import os

import requests


def moderation_reason_embedding(reason):
    response = requests.post("https://language.googleapis.com/v1/documents:analyzeEntities",
        params={"key": os.environ["GOOGLE_LANGUAGE_API_KEY"]},
        json={"document": {"type": "PLAIN_TEXT", "content": reason}, "encodingType": "UTF8"}, timeout=30)
    response.raise_for_status()
    return response.json()["entities"]