import requests


def moderate_claims(text):
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
