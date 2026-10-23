import requests


def visual_safety_text(text: str):
    url = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        params={"key": None},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
    )
    return response.json()
