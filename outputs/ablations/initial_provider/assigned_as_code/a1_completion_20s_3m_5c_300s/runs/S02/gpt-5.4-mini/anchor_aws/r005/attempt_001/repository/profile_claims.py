import requests

from identity_client import get_cognito_base_url, get_oauth_config
from identity_models import normalize_profile_claims


def profile_claims(payload, config=None):
    cfg = get_oauth_config(config)
    access_token = payload["access_token"]
    response = requests.get(
        get_cognito_base_url(cfg) + "/oauth2/userInfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())
