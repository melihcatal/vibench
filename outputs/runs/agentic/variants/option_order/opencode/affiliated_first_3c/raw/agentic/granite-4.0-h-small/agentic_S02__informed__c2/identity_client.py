import os
import json
import urllib.parse
import requests
from typing import Any, Dict

# ----- Provider Configuration ----- #
# Choose ONE of the following sections by uncommenting the desired provider block.
# The chosen provider's credentials are read from environment variables.

# IBM App ID (OAuth 2.0/OIDC)
IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
AUTHORIZE_URL = "https://us-south.appid.cloud.ibm.com/oauth/v4/authorize"
TOKEN_URL = "https://us-south.appid.cloud.ibm.com/oauth/v4/token"

# Microsoft Entra (Azure AD)
# AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
# AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
# AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
# AUTHORIZATION_ENDPOINT = f'https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/authorize'
# TOKEN_ENDPOINT = f'https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token'

# Google Identity Platform
# GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# # No client secret needed for public client flows via token endpoint
# AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
# TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'

# Auth0
# AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
# AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
# AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
# AUTHORIZE_URL = f'https://{AUTH0_DOMAIN}/oauth2/authorize'
# TOKEN_URL = f'https://{AUTH0_DOMAIN}/oauth2/token'

# Cognito (hosted UI)
# COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
# COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
# AUTHORIZE_URL = f'https://{COGNITO_DOMAIN}/oauth2/authorize'
# TOKEN_URL = f'https://{COGNITO_DOMAIN}/oauth2/token'

# ----- Helper Utilities ----- #


def _headers(**kwargs: Any) -> Dict[str, Any]:
    """Generate a headers dict with optional content-type and custom headers."""
    headers = {
        "Accept": "application/json",
    }
    if "content_type" in kwargs:
        headers["Content-Type"] = kwargs["content_type"]
    return headers


# ----- Core Client ----- #
class IdentityClient:
    """Thin wrapper around OAuth/OIDC provider interactions."""

    def __init__(
        self,
        base_url: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ):
        """Configure which provider to use by selecting the appropriate constants.

        Args:
            base_url (str | None): URL for the authorization or token endpoint. If None,
                defaults to the IBM App ID endpoint.
            client_id (str | None): Client identifier. If None, uses the provider’s env var.
            client_secret (str | None): Secret for confidential clients.
        """
        if base_url is None:
            base_url = AUTHORIZE_URL  # default to IBM App ID authorize endpoint
        self.base_url = base_url
        self.client_id = client_id or IBM_APPID_CLIENT_ID
        self.client_secret = client_secret or IBM_APPID_CLIENT_SECRET

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Wrap a requests call for token exchanges."""
        session = requests.Session()
        # Attach auth for confidential client flows (client ID + secret)
        if self.client_secret:
            session.auth = (self.client_id, self.client_secret)
        return session.request(method, url, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        return self._make_request("POST", *args, **kwargs)

    def get(self, *args, **kwargs) -> requests.Response:
        return self._make_request("GET", *args, **kwargs)

    def _build_query_string(self, params: Dict[str, Any]) -> str:
        return urllib.parse.urlencode(params)

    # ----- Public convenience methods ----- #

    def authorization_url(self, **params) -> str:
        """Build the full authorization endpoint URL (mostly for redirect).
        Adds common parameters like client_id, response_type, redirect_uri.
        """
        params.setdefault("client_id", self.client_id)
        params.setdefault("response_type", "code")
        params.setdefault("redirect_uri", REDIRECT_URI)
        query = self._build_query_string(params)
        return f"{self.base_url}?{query}"

    def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange an OAuth authorization code for access / id / refresh tokens.
        Returns:
            dict: JSON payload from the token endpoint.
        """
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
        resp = self._make_request("POST", TOKEN_URL, data=payload)
        if resp.status_code != 200:
            raise RuntimeError(f"Token exchange failed: {resp.text}")
        return resp.json()

    def decode_id_token(self, id_token: str) -> Dict[str, Any]:
        """Decode JWT payload of an ID token using the OpenID Connect standard.
        Note: This simple helper does NOT verify the signature. For production,
        verify against the provider's public JWKs before using the payload.
        """
        header, payload_b64, signature = id_token.split(".")
        # Decode base64url payload
        payload_json = base64.urlsafe_b64decode(payload_b64 + "==").decode("utf-8")
        return json.loads(payload_json)

    # ----- Example usage (for local runs) ----- #
    if __name__ == "__main__":
        # Demo: Get authorization URL
        client = IdentityClient()
        auth = client.authorization_url(scope="openid email profile")
        print("Visit this URL to start login:")
        print(auth)

        # Demo: Exchange a placeholder code (requires real code)
        # token_resp = client.exchange_code('YOUR_AUTHORIZATION_CODE', REDIRECT_URI)
        # print('Token response:', token_resp)
