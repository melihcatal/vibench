import os
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

def handle_auth0_callback(auth_code: str):
    """Handles the Auth0 callback and exchanges the authorization code for tokens."""
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 environment variables.")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': auth_code,
        'redirect_uri': AUTH0_CALLBACK_URL
    }

    try:
        response = requests.post(token_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        return None

if __name__ == "__main__":
    # Example usage (in a real app, this would come from the redirect URL)
    example_auth_code = "YOUR_AUTHORIZATION_CODE_HERE"
    tokens = handle_auth0_callback(example_auth_code)
    if tokens:
        print("Successfully received tokens:")
        print(json.dumps(tokens, indent=2))
