import requests
import os
from identity_models import UserProfile


def fetch_profile_claims(access_token: str) -> UserProfile:
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    userinfo_url = f"https://{auth0_domain}/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    return UserProfile(
        sub=data.get("sub"),
        name=data.get("name"),
        email=data.get("email"),
        email_verified=data.get("email_verified", False),
        picture=data.get("picture")
    )