import requests


def live_caption_safety(text: str):
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    response = requests.post(
        endpoint,
        params={"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
