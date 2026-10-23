import requests


def claims_moderation(payload, config=None):
    api_key = (config or {}).get("perspective_api_key")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": payload["text"]},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
