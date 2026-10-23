import requests

from identity_client import load_identity_config
from identity_models import normalize_claims


def fetch_profile_claims(access_token: str):
    cfg = load_identity_config()
    response = requests.get(
        f"https://{cfg['cognito_domain']}/oauth2/userInfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    return normalize_claims(response.json())
