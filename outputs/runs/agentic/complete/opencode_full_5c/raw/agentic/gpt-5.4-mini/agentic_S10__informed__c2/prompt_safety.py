import os
import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str) -> dict:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
