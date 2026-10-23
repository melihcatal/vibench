import requests
import os
from typing import Dict, Any


# Auth0 OAuth2 Provider Configuration
def get_auth0_config():
    return {
        "api_base_url": "https://dev-12345678.auth0.com/",
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
    }


def fetch_profile_claims(access_token: str) -> Dict[str, Any]:
    config = get_auth0_config()
    url = f"{config['api_base_url']}userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize Auth0 claims to a standard format
    normalized_claims = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "updated_at": claims.get("updated_at"),
    }
    return normalized_claims
