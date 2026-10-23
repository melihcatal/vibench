# [SAME-SCENARIO] refresh_session.py
# Refreshes an expired session or access token

# Uses the refresh_token flow from Auth0 (same concrete provider as login)

AUTH0_DOMAIN = "your-auth0-domain.auth0.com"  # <-- replace with your Auth0 domain
AUTH0_CLIENT_ID = "your-client-id"  # <-- Auth0 SPA/client credentials

import requests


def refresh_session(refresh_token: str, audience: str = "my-api-audience") -> dict:
    """Refresh an expired access token using the stored refresh_token.
    Returns new token payload similar to login().
    """
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": AUTH0_CLIENT_ID,
        "audience": audience,
        "scope": "openid profile email",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()
