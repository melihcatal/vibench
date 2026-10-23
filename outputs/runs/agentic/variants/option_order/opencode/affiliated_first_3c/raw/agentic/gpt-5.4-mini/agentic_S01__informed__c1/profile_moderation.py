import requests
from identity_client import load_identity_config


def profile_moderation(text: str) -> dict:
    config = load_identity_config()
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}}}
    response = requests.post(endpoint, params={"key": config.auth0_client_secret}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
