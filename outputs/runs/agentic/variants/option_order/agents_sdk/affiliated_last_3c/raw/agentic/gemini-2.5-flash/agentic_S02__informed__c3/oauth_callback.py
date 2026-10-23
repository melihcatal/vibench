import os
import requests
import json

def handle_auth0_callback(auth_code: str, state: str) -> dict:
    """
    Handles the Auth0 callback, exchanges the authorization code for tokens.

    Args:
        auth_code: The authorization code received from Auth0.
        state: The state parameter received from Auth0 (for CSRF protection).

    Returns:
        A dictionary containing the ID token, access token, and refresh token.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    # In a real application, validate the 'state' parameter against the one sent in the authorization request.
    # For this example, we'll skip state validation for brevity.

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": AUTH0_CALLBACK_URL
    }

    response = requests.post(token_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status() # Raise an exception for HTTP errors

    tokens = response.json()
    return {
        "id_token": tokens.get("id_token"),
        "access_token": tokens.get("access_token"),
        "refresh_token": tokens.get("refresh_token"),
        "expires_in": tokens.get("expires_in")
    }

if __name__ == "__main__":
    # Example usage (not part of the core logic)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"

    dummy_auth_code = "dummy_auth_code_from_auth0"
    dummy_state = "some_random_state_string_for_csrf_protection"
    try:
        # This call will likely fail without a valid code and actual Auth0 setup
        # but demonstrates the function call structure.
        token_data = handle_auth0_callback(dummy_auth_code, dummy_state)
        print(f"Successfully exchanged code for tokens: {token_data}")
    except Exception as e:
        print(f"Error during token exchange: {e}")
