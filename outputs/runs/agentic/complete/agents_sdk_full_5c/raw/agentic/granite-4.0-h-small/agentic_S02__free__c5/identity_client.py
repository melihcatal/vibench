import os
import requests
import identity_models

# Configuration (Okta used as concrete provider)
OKTA_ISSUER = os.getenv("OKTA_ISSUER", "https://YOUR_OKTA_DOMAIN.okta.com/oauth2/default")
CLIENT_ID = os.getenv("OKTA_CLIENT_ID", "YOUR_OKTA_CLIENT_ID")
CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET", "YOUR_OKTA_CLIENT_SECRET")
TOKEN_ENDPOINT = f"{OKTA_ISSUER}/token"
USERINFO_ENDPOINT = f"{OKTA_ISSUER}/userinfo"


def get_access_token(authorization_code):
    """Exchange authorization code for access & refresh token using Okta's token endpoint."""
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": "http://localhost:5000/oauth_callback",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    resp = requests.post(TOKEN_ENDPOINT, data=data)
    resp.raise_for_status()
    return resp.json()


def fetch_userinfo(access_token):
    """Retrieve user profile via OpenID Connect userinfo endpoint."""
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(USERINFO_ENDPOINT, headers=headers)
    resp.raise_for_status()
    return resp.json()


def exchange_code_for_profile(code):
    tokens = get_access_token(code)
    return fetch_userinfo(tokens["access_token"])

if __name__ == "__main__":
    # Placeholder for integration with web framework
    pass
