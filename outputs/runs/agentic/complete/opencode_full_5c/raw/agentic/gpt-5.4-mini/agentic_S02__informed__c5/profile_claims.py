import requests

from identity_client import load_identity_config, userinfo_endpoint
from identity_models import normalize_claims


def fetch_profile_claims(access_token: str) -> dict:
    config = load_identity_config("AUTH0")
    response = requests.get(
        userinfo_endpoint(config),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return normalize_claims(response.json())
