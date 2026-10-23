import os
import requests
import json

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

def handle_oauth_callback(authorization_code: str) -> dict:
    """
    Handles the OAuth/OIDC callback and exchanges an authorization code for tokens.

    Args:
        authorization_code: The authorization code received from the identity provider.

    Returns:
        A dictionary containing the access, ID, and refresh tokens.
    """
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL]):
        raise ValueError("Auth0 environment variables not set.")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        tokens = response.json()
        return {
            "access_token": tokens.get("access_token"),
            "id_token": tokens.get("id_token"),
            "refresh_token": tokens.get("refresh_token"),
            "expires_in": tokens.get("expires_in")
        }
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging authorization code for tokens: {e}")
        raise

