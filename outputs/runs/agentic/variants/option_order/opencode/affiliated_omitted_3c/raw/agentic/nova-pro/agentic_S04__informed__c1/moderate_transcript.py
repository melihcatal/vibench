import os
import requests


def moderate_transcript(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(url, json=payload)
    return response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.5
