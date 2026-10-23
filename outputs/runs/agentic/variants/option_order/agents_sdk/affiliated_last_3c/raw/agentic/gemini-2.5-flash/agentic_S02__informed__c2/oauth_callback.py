import os
import json
import requests

def handle_oauth_callback(authorization_code: str):
    """
    Handles the OAuth 2.0 Authorization Code Flow callback, exchanges the code for tokens,
    and returns the ID token and access token.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 environment variables.")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging authorization code: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    # Example usage (in a web application, this would be called from the callback endpoint)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.us.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"
    
    # Simulate an authorization code received from the IDP
    mock_auth_code = "mock_auth_code_from_idp" 
    try:
        tokens = handle_oauth_callback(mock_auth_code)
        print("Successfully obtained tokens:")
        print(json.dumps(tokens, indent=2))
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Runtime Error: {e}")
