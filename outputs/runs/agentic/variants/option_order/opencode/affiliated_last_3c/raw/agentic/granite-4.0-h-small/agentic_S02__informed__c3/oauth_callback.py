import os
import requests
from identity_client import IdentityClient
from identity_models import OAuthTokenResponse, AuthorizationCodeGrantRequest

# Google Identity Platform OIDC example
GOOGLE_IDP_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def oauth_callback(code: str, redirect_uri: str) -> OAuthTokenResponse:
    """Exchange the OAuth authorization code for access and ID tokens.
    Returns an OAuthTokenResponse containing the tokens.
    """
    token_endpoint = GOOGLE_IDP_TOKEN_ENDPOINT
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_endpoint, data=data, timeout=10)
    response.raise_for_status()
    body = response.json()
    return OAuthTokenResponse(**body)
