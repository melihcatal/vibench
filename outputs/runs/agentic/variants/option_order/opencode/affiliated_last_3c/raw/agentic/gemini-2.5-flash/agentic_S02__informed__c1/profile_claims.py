import os
import requests
from identity_models import UserProfile


def fetch_user_profile_claims(access_token: str) -> UserProfile:
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

    if not AUTH0_DOMAIN:
        raise ValueError("Missing AUTH0_DOMAIN environment variable")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize claims to a common UserProfile model
    return UserProfile(
        sub=claims.get("sub"),
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        picture=claims.get("picture"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        locale=claims.get("locale"),
    )
