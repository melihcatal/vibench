import requests

from identity_client import Auth0Config, auth0_userinfo_endpoint
from identity_models import UserClaims, normalize_claims


def profile_claims(access_token: str) -> UserClaims:
    cfg = Auth0Config()
    response = requests.get(
        auth0_userinfo_endpoint(cfg),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return normalize_claims(response.json())
