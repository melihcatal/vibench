import os
import requests


def moderate_text(text: str):
    # Using Perspective API for text moderation
    # https://developers.perspectiveapi.com/s/docs
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}

    response = requests.post(url, json=data)
    response.raise_for_status()

    return response.json()
