import requests

from identity_client import load_identity_config
from identity_models import normalize_profile_claims


def profile_claims(payload, config=None):
    config = load_identity_config(config)
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())
