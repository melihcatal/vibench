import requests


def secret_label_safety(text: str) -> dict:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": "", "alt": "json"},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    return response.json()
