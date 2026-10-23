import os
import requests
from typing import Dict, Any
from identity_models import UserProfile

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")


def fetch_user_profile_claims(access_token: str) -> UserProfile:
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN must be set in environment variables.")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    claims: Dict[str, Any] = response.json()

    # Normalize claims to a common UserProfile structure
    return UserProfile(
        sub=claims.get("sub", ""),
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        picture=claims.get("picture"),
        raw_claims=claims,
    )
