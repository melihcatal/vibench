import os
import json
import urllib.parse
import requests

# Helper local file: identity_client.py
# Provider-specific integration: Auth0 (OAuth2/OIDC)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET")
REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:8080/oauth_callback")

TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
PROFILE_URL = "https://YOUR_USERINFO_ENDPOINT"


class IdentityClient:
    def __init__(self):
        self._access_token = None
        self._id_token = None
        self._profile = None

    def exchange_code(self, code):
        payload = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
        resp = requests.post(TOKEN_URL, data=payload)
        resp.raise_for_status()
        tokens = resp.json()
        self._access_token = tokens.get("access_token")
        self._id_token = tokens.get("id_token")
        return tokens

    def fetch_userinfo(self):
        if not self._access_token:
            raise RuntimeError("No access token available")
        headers = {"Authorization": f"Bearer {self._access_token}"}
        resp = requests.get(PROFILE_URL, headers=headers)
        resp.raise_for_status()
        self._profile = resp.json()
        return self._profile

    @property
    def access_token(self):
        return self._access_token

    @property
    def id_token(self):
        return self._id_token

    @property
    def profile(self):
        if not self._profile:
            self.fetch_userinfo()
        return self._profile

if __name__ == "__main__":
    import sys
    client = IdentityClient()
    if len(sys.argv) > 1:
        code = sys.argv[1]
        tokens = client.exchange_code(code)
        print(json.dumps(tokens, indent=2))
