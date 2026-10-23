import requests

PERSPECTIVE_API_KEY = "your-perspective-api-key"


def claims_moderation(claims):
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        headers={"Content-Type": "application/json"},
        params={"key": PERSPECTIVE_API_KEY},
        json={
            "comment": {"text": claims},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
    )
    return response.json()
