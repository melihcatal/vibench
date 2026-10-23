import requests
import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "https://example.auth0.com")


def fetch_auth0_profile(token):
    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }
    response = requests.get(f"{AUTH0_DOMAIN}/userinfo", headers=headers)
    response.raise_for_status()
    claims = response.json()
    
    normalized = {
        "id": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "picture": claims.get("picture"),
        "provider": "auth0"
    }
    return normalized