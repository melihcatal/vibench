import requests


def visual_safety_text(text):
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": "PERSPECTIVE_API_KEY"},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
    )
    response.raise_for_status()
    return response.json()
