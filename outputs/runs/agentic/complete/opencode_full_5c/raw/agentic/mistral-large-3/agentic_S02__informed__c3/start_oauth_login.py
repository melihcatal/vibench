from typing import Dict, Optional
import os
import requests
from urllib.parse import urlencode

# Google Identity Platform OIDC
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_SCOPES = ["openid", "profile", "email"]


def start_oauth_login(state: str, code_challenge: Optional[str] = None) -> str:
    # Fetch Google's OIDC configuration
    discovery_doc = requests.get(GOOGLE_DISCOVERY_URL).json()
    auth_endpoint = discovery_doc["authorization_endpoint"]

    # Build the authorization request
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "state": state,
    }

    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"

    auth_url = f"{auth_endpoint}?{urlencode(params)}"
    return auth_url
