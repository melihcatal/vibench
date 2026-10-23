import requests


def profile_moderation(text: str):
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}},
        },
        timeout=30,
    )
    return response.json()
