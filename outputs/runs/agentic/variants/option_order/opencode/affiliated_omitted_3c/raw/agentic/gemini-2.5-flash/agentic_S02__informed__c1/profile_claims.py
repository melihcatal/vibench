import os
import requests
import json

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


def fetch_and_normalize_profile_claims(access_token: str):
    if not AUTH0_DOMAIN:
        raise ValueError("Missing AUTH0_DOMAIN environment variable")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize claims (example)
    normalized_claims = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
    }
    return normalized_claims
