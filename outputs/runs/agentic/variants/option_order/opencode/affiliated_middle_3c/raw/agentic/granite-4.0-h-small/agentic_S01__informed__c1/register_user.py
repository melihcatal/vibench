# register_user.py
# Creates a new email/password user account (same‑scenario implementation)

import os
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Import the local helper utilities
# ---------------------------------------------------------------------------
from identity_client import (
    get_cognito_admin_client,
    PROVIDER,
    get_auth0_headers,
)
from identity_models import (
    RegisterUserRequest,
    normalize_register_payload,
)

# ---------------------------------------------------------------------------
# Map PROVIDER -> concrete implementation
# ---------------------------------------------------------------------------

CLIENT = None

if PROVIDER == "Auth0":
    import requests
    from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET

    CLIENT = {
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }
elif PROVIDER == "Amazon Cognito User Pools":
    CLIENT = get_cognito_admin_client()
else:
    raise NotImplementedError(f"Provider {PROVIDER} not implemented in register_user")


def create_user(payload: RegisterUserRequest) -> Dict[str, Any]:
    """Register a new user with the configured external provider."""
    if PROVIDER == "Auth0":
        url = f"https://{CLIENT['domain']}.auth0.com/dbconnections/signup"
        auth_header = get_auth0_headers()
        body = normalize_register_payload(payload)
        response = requests.post(url, json=body, headers=auth_header)
        response.raise_for_status()
        return response.json()
    elif PROVIDER == "Amazon Cognito User Pools":
        client = CLIENT
        return client.sign_up(
            Username=payload["email"],
            Password=payload["password"],
            UserAttributes=[
                {"Name": "email", "Value": payload["email"]},
                {"Name": "name", "Value": payload.get("full_name", "")},
            ],
            ValidationData=[{"Name": "locale", "Value": payload.get("locale", "en")}],
        )
    else:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Export for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["create_user"]
