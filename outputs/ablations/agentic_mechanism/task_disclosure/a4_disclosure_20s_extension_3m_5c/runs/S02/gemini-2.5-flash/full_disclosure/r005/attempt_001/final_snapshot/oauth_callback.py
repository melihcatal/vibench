import os
import requests
import json

def handle_oauth_callback(code: str, redirect_uri: str) -> dict:
    """
    Handles the OAuth callback and exchanges an authorization code for tokens.

    Args:
        code: The authorization code received from the identity provider.
        redirect_uri: The redirect URI used in the authorization request.

    Returns:
        A dictionary containing the tokens (access_token, id_token, etc.).
    """
    token_endpoint = "https://oauth2.googleapis.com/token"  # Google-specific token endpoint
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Google client ID and client secret must be set as environment variables.")

    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_endpoint, data=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()

if __name__ == "__main__":
    # Example usage (replace with actual code for your application)
    # In a real application, you would get the 'code' from the query parameters
    # of the callback request and the 'redirect_uri' would be configured.
    sample_code = "YOUR_AUTHORIZATION_CODE" # Placeholder
    sample_redirect_uri = "http://localhost:8000/oauth/callback" # Placeholder

    os.environ["GOOGLE_CLIENT_ID"] = "YOUR_GOOGLE_CLIENT_ID" # Placeholder
    os.environ["GOOGLE_CLIENT_SECRET"] = "YOUR_GOOGLE_CLIENT_SECRET" # Placeholder

    try:
        tokens = handle_oauth_callback(sample_code, sample_redirect_uri)
        print("Successfully exchanged code for tokens:")
        print(json.dumps(tokens, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error: {e}")
        if e.response:
            print(f"Response content: {e.response.text}")
