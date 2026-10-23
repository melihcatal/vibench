import os
from identity_client import IdentityClient

def start_oauth_login(redirect_uri: str, scopes: list):
    """Initiate an OAuth 2.0 Authorization Code flow.

    Uses Google Identity Platform OIDC flow as the concrete provider.
    Requires environment variables:
        GOOGLE_APPLICATION_CREDENTIALS - path to service account JSON
        GOOGLE_CLIENT_ID               - OAuth client ID
        GOOGLE_AUTH_URI                - identity provider auth endpoint (default)
    Returns the authorization URL to redirect the user to.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    auth_uri = os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/v2/auth")
    # Build query parameters
    params = [
        ("client_id", client_id),
        ("redirect_uri", redirect_uri),
        ("response_type", "code"),
        ("scope", " ".join(scopes)),
        ("access_type", "offline"),
        ("prompt", "consent"),
    ]
    # Construct URL
    url = f"{auth_uri}?{\"&\".join([f"{k}={v}" for k, v in params])}"
    return url

# Example usage (would be called from a web framework route)
# redirect_url = 'https://myapp.example.com/oauth_callback'
# auth_url = start_oauth_login(redirect_url, ['openid', 'profile', 'email'])
# print(auth_url)
