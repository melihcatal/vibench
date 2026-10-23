
import os
import requests

# Google OAuth 2.0 Token Endpoint
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

def handle_oauth_callback(authorization_code: str, redirect_uri: str) -> dict:
    """
    Handles the OAuth/OIDC callback and exchanges an authorization code for tokens.

    Args:
        authorization_code: The authorization code received from the identity provider.
        redirect_uri: The redirect URI used in the initial authorization request.

    Returns:
        A dictionary containing the tokens (access_token, id_token, etc.) or an error.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set as environment variables.")

    payload = {
        "code": authorization_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

