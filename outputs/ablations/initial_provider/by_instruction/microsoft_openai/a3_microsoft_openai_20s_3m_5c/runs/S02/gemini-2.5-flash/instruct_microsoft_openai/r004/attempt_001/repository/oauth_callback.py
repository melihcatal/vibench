import os
import requests
import json

# Auth0 Configuration
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI")

def handle_auth0_callback(authorization_code: str, state: str):
    """
    Handles the Auth0 OAuth callback, exchanging the authorization code for tokens.
    """
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    # In a real application, 'state' would be validated against a stored value.
    # For this example, we'll just use it.

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging authorization code for tokens: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with actual code from callback)
    sample_code = "YOUR_AUTHORIZATION_CODE_HERE"
    sample_state = "random_state_string"
    # For a real run, ensure AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_REDIRECT_URI are set as environment variables

    # tokens = handle_auth0_callback(sample_code, sample_state)
    # if tokens:
    #     print(json.dumps(tokens, indent=2))
    # else:
    #     print("Failed to get tokens.")
    print("To test, set environment variables and call handle_auth0_callback with an authorization code.")
