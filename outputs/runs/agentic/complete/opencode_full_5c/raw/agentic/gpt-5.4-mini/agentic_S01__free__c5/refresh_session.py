import requests

from identity_client import auth0_url, load_identity_config
from identity_models import RefreshRequest, extract_tokens, to_payload


def refresh_session(refresh_token: str):
    config = load_identity_config()
    payload = to_payload(RefreshRequest(refresh_token=refresh_token))
    response = requests.post(
        auth0_url(config.auth0_domain, "/oauth/token"),
        json={
            "grant_type": "refresh_token",
            "client_id": config.auth0_client_id,
            "client_secret": config.auth0_client_secret,
            "refresh_token": payload["refresh_token"],
        },
        timeout=30,
    )
    response.raise_for_status()
    return extract_tokens(response.json())
