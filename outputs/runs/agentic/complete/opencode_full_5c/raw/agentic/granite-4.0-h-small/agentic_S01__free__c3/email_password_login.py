# [SAME-SCENARIO] email_password_login.py
# Signs in a user with email and password and returns tokens

# Example integration using a concrete provider (Auth0 Authorization Code Flow for email/password)

AUTH0_DOMAIN = "your-auth0-domain.auth0.com"  # <-- replace with your Auth0 domain
AUTH0_CLIENT_ID = "your-client-id"  # <-- Auth0 SPA/client credentials

import requests
import uuid


def email_password_login(
    email: str, password: str, audience: str = "my-api-audience"
) -> dict:
    """Authenticate with email/password using Auth0's /oauth/token endpoint and return tokens.
    Returns a dict with 'access_token', 'id_token', 'refresh_token', and 'expires_in'.
    """
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": audience,
        "scope": "openid profile email",
        "client_id": AUTH0_CLIENT_ID,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()


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
