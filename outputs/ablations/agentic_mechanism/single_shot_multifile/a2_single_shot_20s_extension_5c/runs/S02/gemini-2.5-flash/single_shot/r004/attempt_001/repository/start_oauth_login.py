import os

from urllib.parse import urlencode

from identity_client import OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_REDIRECT_URI

def start_okta_login(state: str, scope: str = "openid profile email") -> str:
    """Constructs the Okta authorization URL for the OAuth 2.0 authorization code flow."""
    auth_params = {
        "client_id": OKTA_CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": OKTA_REDIRECT_URI,
        "state": state,
    }
    
    # Okta's authorization endpoint typically follows this pattern
    authorization_url = f"{OKTA_ORG_URL}/oauth2/default/v1/authorize?{urlencode(auth_params)}"
    return authorization_url
