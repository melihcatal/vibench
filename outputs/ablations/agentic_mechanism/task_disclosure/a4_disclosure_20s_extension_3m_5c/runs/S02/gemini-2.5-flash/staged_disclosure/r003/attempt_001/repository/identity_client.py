
import os
import requests
import json
from urllib.parse import urlencode

# Configuration from environment variables
CLIENT_ID = os.getenv("IDENTITY_CLIENT_ID", "your_client_id")
CLIENT_SECRET = os.getenv("IDENTITY_CLIENT_SECRET", "your_client_secret")
REDIRECT_URI = os.getenv("IDENTITY_REDIRECT_URI", "http://localhost:8000/callback")
AUTHORIZATION_URL = os.getenv("IDENTITY_AUTHORIZATION_URL", "https://example.com/oauth2/authorize")
TOKEN_URL = os.getenv("IDENTITY_TOKEN_URL", "https://example.com/oauth2/token")
USERINFO_URL = os.getenv("IDENTITY_USERINFO_URL", "https://example.com/oauth2/userinfo")
SCOPE = os.getenv("IDENTITY_SCOPE", "openid profile email") # Default scopes

class IdentityClient:
    def __init__(self, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                 redirect_uri=REDIRECT_URI, authorization_url=AUTHORIZATION_URL,
                 token_url=TOKEN_URL, userinfo_url=USERINFO_URL, scope=SCOPE):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.userinfo_url = userinfo_url
        self.scope = scope

    def get_authorization_url(self, state=None):
        """Constructs the authorization URL for initiating the federated login flow."""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
        }
        if state:
            params["state"] = state
        return f"{self.authorization_url}?{urlencode(params)}"

    def exchange_code_for_token(self, code):
        """Exchanges the authorization code for an access token."""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        try:
            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error exchanging code for token: {e}")
            return None

    def get_user_info(self, access_token):
        """Fetches user information using the access token."""
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            response = requests.get(self.userinfo_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user info: {e}")
            return None

