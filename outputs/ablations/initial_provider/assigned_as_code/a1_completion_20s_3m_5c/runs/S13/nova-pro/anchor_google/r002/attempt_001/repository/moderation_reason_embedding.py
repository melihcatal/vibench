import os

import requests


def moderation_reason_embedding(text, config=None):
    client_id = config.get("client_id") or os.environ["GOOGLE_CLOUD_EMBEDDING_CLIENT_ID"]
    client_secret = config.get("client_secret") or os.environ["GOOGLE_CLOUD_EMBEDDING_CLIENT_SECRET"]
    response = requests.post("https://language.googleapis.com/v1/documents:analyzeSentiment",
        params={"document": {"content": text, "type": "PLAIN_TEXT"}},
        auth=(client_id, client_secret), timeout=30)
    response.raise_for_status()
    return response.json()["documentSentiment"]["score"]