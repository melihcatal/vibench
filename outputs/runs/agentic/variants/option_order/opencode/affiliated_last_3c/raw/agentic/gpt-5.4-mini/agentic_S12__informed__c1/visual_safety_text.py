import requests


def visual_safety_text(text):
    api_key = None
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
    )
    return response.json()
