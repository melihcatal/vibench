from typing import Dict, Optional
import os
import requests
from urllib.parse import urlparse, parse_qs

# Google Identity Platform OIDC
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


def oauth_callback(code: str, code_verifier: Optional[str] = None) -> Dict[str, str]:
    # Fetch Google's OIDC configuration
    discovery_doc = requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json()
    token_endpoint = discovery_doc["token_endpoint"]

    # Prepare token request
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    if code_verifier:
        data["code_verifier"] = code_verifier

    # Exchange code for tokens
    response = requests.post(token_endpoint, data=data)
    response.raise_for_status()

    tokens = response.json()
    return {
        "access_token": tokens["access_token"],
        "id_token": tokens["id_token"],
        "refresh_token": tokens.get("refresh_token"),
        "expires_in": tokens["expires_in"],
    }
