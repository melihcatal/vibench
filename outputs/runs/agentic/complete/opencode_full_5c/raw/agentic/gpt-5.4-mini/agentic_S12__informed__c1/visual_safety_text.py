import requests


def visual_safety_text(text):
    api_key = ""
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        params={"key": api_key},
    )
    return response.json()
