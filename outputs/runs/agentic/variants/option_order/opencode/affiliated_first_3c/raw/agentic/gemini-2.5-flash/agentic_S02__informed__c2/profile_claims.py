import os
import requests


def fetch_auth0_profile_claims(access_token: str):
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")

    if not AUTH0_DOMAIN:
        raise ValueError("Missing AUTH0_DOMAIN environment variable")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    return response.json()
