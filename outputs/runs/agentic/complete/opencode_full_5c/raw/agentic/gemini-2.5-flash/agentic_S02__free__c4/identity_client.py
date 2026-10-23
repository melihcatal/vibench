import os
import requests
from urllib.parse import urlencode


class IdentityClientConfig:
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get(
        "GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET"
    )
    GOOGLE_REDIRECT_URI = os.environ.get(
        "GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback"
    )
    OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID", "YOUR_OKTA_CLIENT_ID")
    OKTA_ISSUER = os.environ.get(
        "OKTA_ISSUER", "https://{your-okta-domain}/oauth2/default"
    )
    OKTA_REDIRECT_URI = os.environ.get(
        "OKTA_REDIRECT_URI", "http://localhost:8000/pkce_callback"
    )

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def generate_google_auth_url(state: str, scope: str = "openid email profile"):
    params = {
        "client_id": IdentityClientConfig.GOOGLE_CLIENT_ID,
        "redirect_uri": IdentityClientConfig.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": scope,
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{IdentityClientConfig.GOOGLE_AUTH_URL}?{urlencode(params)}"
