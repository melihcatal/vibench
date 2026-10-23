import os
import urllib.parse

# Google OAuth 2.0 Endpoints and client configuration
GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback")
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

def start_oauth_login(state: str) -> str:
    """
    Starts an OAuth or OIDC authorization-code login flow by constructing the
    authorization URL for Google.

    Args:
        state: A unique, opaque string used to maintain state between the request
               and the callback. It helps prevent cross-site request forgery.

    Returns:
        The authorization URL to redirect the user to.
    """
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "access_type": "offline",
        "state": state,
        "prompt": "consent",
    }
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"{GOOGLE_AUTHORIZATION_ENDPOINT}?{query_string}"
    return authorization_url
