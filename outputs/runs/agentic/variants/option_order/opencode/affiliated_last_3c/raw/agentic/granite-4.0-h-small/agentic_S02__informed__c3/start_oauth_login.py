import os
import requests
from identity_client import IdentityClient
from identity_models import OAuthAuthorizationResponse

# Google Identity Platform OIDC example
GOOGLE_IDP_ISSUER = "https://accounts.google.com"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def start_oauth_login(redirect_uri: str) -> str:
    """Redirect user to Google's consent screen to start OAuth login.
    Returns a fully qualified authorization URL.
    """
    auth_endpoint = f"{GOOGLE_IDP_ISSUER}/o/oauth2/v2/auth?"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid email profile",
    }
    return auth_endpoint + requests.compat.urlencode(params)
