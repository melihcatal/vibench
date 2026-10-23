import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def claims_moderation(text: str) -> dict:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": "${PERSPECTIVE_API_KEY}"},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
