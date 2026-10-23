# refresh_session.py
# Refreshes an expired session or access token (Auth0 reference)

import os
import json
from typing import Dict, Any
from identity_client import create_client
from identity_models import RefreshTokenRequest, AuthSuccess

# Auth0 credentials (set as environment variables)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
    raise RuntimeError("Set AUTH0_DOMAIN and AUTH0_CLIENT_ID env vars")

TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"

headers = {
    "Content-Type": "application/json",
}


def refresh_session(payload: RefreshTokenRequest) -> AuthSuccess:
    """Exchange a refresh token for a new access/refresh token pair."""
    payload_dict = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": payload.refresh_token,
        "scope": "openid profile email",
    }
    resp = __import__("requests").post(TOKEN_URL, data=payload_dict, headers=headers)
    resp.raise_for_status()
    token_data = resp.json()
    return AuthSuccess(**token_data)


# Example usage (do not run in production script)
if __name__ == "__main__":
    req = RefreshTokenRequest(refresh_token="old.refresh.token.string")
    tokens = refresh_session(req)
    print(json.dumps(tokens.to_dict(), indent=2))
