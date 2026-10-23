import requests
from identity_client import get_identity_config
from identity_models import NormalizedProfile

def fetch_normalized_profile(token: str) -> NormalizedProfile:
    config = get_identity_config()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "https://dev-12345678.us.auth0.com/userinfo",
        headers=headers,
    )
    response.raise_for_status()
    claims = response.json()
    return NormalizedProfile(
        sub=claims.get("sub"),
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified", False),
        picture=claims.get("picture"),
    )