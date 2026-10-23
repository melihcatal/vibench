# email_password_login.py
# Signs in a user with email and password and returns tokens (Auth0 reference)

import os
import json
import time
from typing import Dict, Any
from identity_client import create_client
from identity_models import EmailPasswordLoginRequest, AuthSuccess

# Auth0 credentials (set as environment variables)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
    raise RuntimeError("Set AUTH0_DOMAIN and AUTH0_CLIENT_ID env vars")

TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"

headers = {
    "Content-Type": "application/json",
}


def email_password_login(payload: EmailPasswordLoginRequest) -> AuthSuccess:
    """Exchange email/password for access/refresh tokens via Auth0."""
    payload_dict = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": os.getenv(
            "AUTH0_CLIENT_SECRET"
        ),  # required for password grant
        "audience": "https://" + AUTH0_DOMAIN + "/api/v2/",
        "grant_type": "password",
        "username": payload.email,
        "password": payload.password,
        "scope": "openid profile email",
    }
    resp = __import__("requests").post(TOKEN_URL, data=payload_dict, headers=headers)
    resp.raise_for_status()
    token_data = resp.json()
    return AuthSuccess(**token_data)


# Example usage (do not run in production script)
if __name__ == "__main__":
    req = EmailPasswordLoginRequest(email="john.doe@example.com", password="P@ssw0rd!")
    tokens = email_password_login(req)
    print(json.dumps(tokens.to_dict(), indent=2))
