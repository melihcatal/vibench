import os
import requests
import json

def handle_oauth_callback(authorization_code: str, redirect_uri: str) -> dict:
    """
    Handles the OAuth/OIDC callback, exchanging an authorization code for tokens.
    Uses Google as the concrete external provider.
    """
    google_client_id = os.environ.get("GOOGLE_CLIENT_ID")
    google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    google_token_url = "https://oauth2.googleapis.com/token" # Google's token endpoint

    if not google_client_id or not google_client_secret:
        raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables must be set.")

    token_payload = {
        "client_id": google_client_id,
        "client_secret": google_client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(google_token_url, data=token_payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging authorization code for tokens: {e}")
        raise

