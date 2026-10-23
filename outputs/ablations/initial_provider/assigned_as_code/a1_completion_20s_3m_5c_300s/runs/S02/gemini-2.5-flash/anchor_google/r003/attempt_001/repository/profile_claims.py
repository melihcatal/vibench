import requests
from typing import Dict, Any

from identity_models import UserProfile
from identity_client import get_auth0_config

def fetch_user_profile_claims(access_token: str) -> UserProfile:
    config = get_auth0_config()
    domain = config["AUTH0_DOMAIN"]

    userinfo_url = f"https://{domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers, timeout=30)
    response.raise_for_status()
    claims = response.json()

    return UserProfile(
        sub=claims.get("sub"),
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        picture=claims.get("picture"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        locale=claims.get("locale"),
        additional_claims={
            k: v for k, v in claims.items() if k not in [
                "sub", "name", "email", "email_verified", "picture",
                "given_name", "family_name", "locale"
            ]
        }
    )
