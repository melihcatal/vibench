
import os
import requests
import json

def refresh_access_token(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token using Auth0.

    Args:
        refresh_token: The refresh token obtained during the initial login.

    Returns:
        A dictionary containing the new access token, ID token, and their expiration.
        Returns an empty dictionary if the refresh fails.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")

    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set.")

    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/json"}
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing token: {e}")
        return {}

