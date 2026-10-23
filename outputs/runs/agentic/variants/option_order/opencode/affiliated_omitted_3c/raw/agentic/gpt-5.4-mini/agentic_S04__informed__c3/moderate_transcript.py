import requests

from speech_client import get_env


def moderate_transcript(text: str = ""):
    api_key = get_env("PERSPECTIVE_API_KEY")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}},
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
