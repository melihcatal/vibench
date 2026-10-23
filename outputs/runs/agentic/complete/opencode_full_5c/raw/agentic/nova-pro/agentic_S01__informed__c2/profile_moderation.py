import os
import requests


def moderate_text(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload)
    return response.json()
