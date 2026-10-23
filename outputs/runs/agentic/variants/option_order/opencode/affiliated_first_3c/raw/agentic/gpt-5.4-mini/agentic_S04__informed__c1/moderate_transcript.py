import requests


def moderate_transcript(text: str) -> dict[str, object]:
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    return requests.post(
        endpoint,
        params={"key": __import__("os").environ.get("PERSPECTIVE_API_KEY", "")},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
    ).json()
