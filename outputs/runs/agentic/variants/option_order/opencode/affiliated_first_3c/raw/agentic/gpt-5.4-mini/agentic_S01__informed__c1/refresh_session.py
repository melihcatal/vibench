import requests
from identity_client import load_identity_config


def refresh_session(refresh_token: str) -> dict:
    config = load_identity_config()
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": config.auth0_client_id,
        "client_secret": config.auth0_client_secret,
    }
    response = requests.post(f"https://{config.auth0_domain}/oauth/token", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
