import os
import requests

def exchange_code_for_tokens(code: str, client_id: str, client_secret: str, redirect_uri: str) -> dict:
    """
    Handles the OAuth callback and exchanges an authorization code for tokens using Google OAuth 2.0.
    """
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    # Example usage:
    # auth_code = "YOUR_AUTHORIZATION_CODE"
    # google_client_id = os.environ.get("GOOGLE_CLIENT_ID")
    # google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    # google_redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")
    #
    # try:
    #     tokens = exchange_code_for_tokens(auth_code, google_client_id, google_client_secret, google_redirect_uri)
    #     print("Tokens:", tokens)
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error exchanging code for tokens: {e}")
    #     print(e.response.json())
    pass
