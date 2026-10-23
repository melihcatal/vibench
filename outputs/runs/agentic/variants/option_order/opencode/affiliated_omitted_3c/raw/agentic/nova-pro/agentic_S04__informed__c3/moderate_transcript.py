import os
import requests


def moderate_transcript(transcript):
    headers = {"Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}"}
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + os.getenv("PERSPECTIVE_API_KEY"),
        json={"comment": {"text": transcript}, "requestedAttributes": {"TOXICITY": {}}},
        headers=headers,
    )
    return response.json()
