import requests

from speech_client import perspective_api_key


def moderate_transcript(text: str):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        url, params={"key": perspective_api_key()}, json=payload, timeout=30
    )
    response.raise_for_status()
    return response.json()
