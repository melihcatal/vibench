# register_user.py
# Creates a new email/password user account (Auth0 reference)

import os
import json
import time
from typing import Dict, Any
from identity_client import create_client
from identity_models import RegisterUserRequest, AuthSuccess

# Auth0 credentials (set as environment variables)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
    raise RuntimeError("Set AUTH0_DOMAIN and AUTH0_CLIENT_ID env vars")

API_URL = f"https://{AUTH0_DOMAIN}"
TOKEN_URL = f"{API_URL}/oauth/token"
USERS_URL = f"{API_URL}/api/v2/users"

# Get Management API token
scope = "create:users"
payload = {
    "client_id": AUTH0_CLIENT_ID,
    "grant_type": "client_credentials",
    "audience": "https://" + AUTH0_DOMAIN + "/api/v2/",
    "scope": scope,
}
resp = __import__("requests").post(TOKEN_URL, data=payload)
resp.raise_for_status()
access_token = resp.json()["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}


def register_user(payload: RegisterUserRequest) -> AuthSuccess:
    """Create a new user via Auth0 Management API and return access/refresh tokens."""
    # Auth0 expects email/password user creation in two steps: create user + call /oauth/token
    # For simplicity, we use the Management API to create the user, then exchange a password grant.
    # Step 1 – create the user (password will be set in the token flow)
    user_data = {
        "email": payload.email,
        "email_verified": False,
        "connection": "Username-Password-Authentication",
        "app_metadata": {
            "onboarding": {
                "notes": payload.notes or "",
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        },
    }
    create_res = __import__("requests").post(USERS_URL, headers=headers, json=user_data)
    create_res.raise_for_status()
    user_id = create_res.json()["user_id"]

    # Step 2 – exchange password for tokens (client credentials flow with user credentials)
    token_payload = {
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
    token_res = __import__("requests").post(
        TOKEN_URL, data=token_payload, headers=headers
    )
    token_res.raise_for_status()
    token_json = token_res.json()
    return AuthSuccess(**token_json)


# Example usage (do not run in production script)
if __name__ == "__main__":
    req = RegisterUserRequest(
        email="jane.doe@example.com", password="P@ssw0rd!", notes="Onboarding started"
    )
    tokens = register_user(req)
    print(json.dumps(tokens.to_dict(), indent=2))
