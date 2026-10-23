import os
import requests

def handle_google_oauth_callback(auth_code: str):
    """
    Handles the Google OAuth 2.0 callback and exchanges the authorization code for tokens.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")
    token_url = "https://oauth2.googleapis.com/token"

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError("Missing Google OAuth environment variables.")

    payload = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Example usage (replace with an actual authorization code from Google)
    example_auth_code = "your_google_auth_code_here"
    try:
        tokens = handle_google_oauth_callback(example_auth_code)
        print("Successfully exchanged code for tokens:")
        print(tokens)
    except requests.exceptions.HTTPError as e:
        print(f"Error during token exchange: {e.response.text}")
    except ValueError as e:
        print(f"Configuration error: {e}")
