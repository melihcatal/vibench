import os
import json
import requests
from urllib.parse import urlencode

class Auth0Callback:
    def __init__(self, domain: str, client_id: str, client_secret: str, redirect_uri: str):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def exchange_code_for_tokens(self, authorization_code: str) -> dict:
        """Exchanges an authorization code for access and ID tokens using Auth0."""
        token_url = f"https://{self.domain}/oauth/token"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
        }

        response = requests.post(token_url, headers=headers, data=urlencode(payload))
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    # Example usage (in a real scenario, the code would come from the URL query parameter)
    # For demonstration, a placeholder code is used. Replace with actual code from the callback URL.
    example_authorization_code = "dummy_auth_code_from_callback_url"

    callback_handler = Auth0Callback(AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL)
    try:
        tokens = callback_handler.exchange_code_for_tokens(example_authorization_code)
        print(json.dumps(tokens, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        if e.response is not None:
            print(e.response.json())
