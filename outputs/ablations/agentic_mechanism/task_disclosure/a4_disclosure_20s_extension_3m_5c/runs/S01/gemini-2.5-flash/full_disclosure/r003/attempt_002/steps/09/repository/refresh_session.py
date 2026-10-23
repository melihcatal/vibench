import os
import requests

def refresh_access_token(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token using Auth0's refresh token flow.

    Args:
        refresh_token: The refresh token obtained during the initial login.

    Returns:
        A dictionary containing the new access token, ID token, and other
        relevant information from the Auth0 token endpoint response.
        Returns an empty dictionary if the refresh fails.
    """
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE") # Optional, but good practice for API access

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET]):
        print("Error: Auth0 environment variables not set.")
        return {}

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "audience": AUTH0_AUDIENCE, # Include if your access token is for an API
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing token: {e}")
        return {}

