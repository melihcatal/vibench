import requests

from identity_client import load_cognito_config
from identity_models import normalize_claims


def fetch_profile_claims(access_token: str):
    config = load_cognito_config()
    response = requests.get(
        f"https://{config.issuer}/oauth2/userInfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return normalize_claims(response.json())
