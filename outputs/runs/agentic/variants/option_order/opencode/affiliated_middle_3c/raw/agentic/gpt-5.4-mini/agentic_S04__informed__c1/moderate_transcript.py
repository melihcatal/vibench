import requests
from speech_client import load_config


def moderate_transcript(text: str) -> dict:
    key = load_config().api_key or ""
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
