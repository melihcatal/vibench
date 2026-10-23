import requests


def profile_moderation(text: str):
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data
