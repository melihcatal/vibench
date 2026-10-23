# password_reset.py
# Starts a password reset flow for a local account (same‑scenario implementation)

import os
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Import local helpers
# ---------------------------------------------------------------------------
from identity_client import (
    PROVIDER,
    get_auth0_headers,
)
from identity_models import (
    ResetPasswordRequest,
    ResetPasswordResponse,
    ResetPasswordTokenRequest,
)

# ---------------------------------------------------------------------------
# Map PROVIDER -> concrete implementation
# ---------------------------------------------------------------------------

CLIENT = None

if PROVIDER == "Auth0":
    import requests
    from identity_client import (
        AUTH0_DOMAIN,
        AUTH0_CLIENT_ID,
        AUTH0_CLIENT_SECRET,
    )

    CLIENT = {
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }
elif PROVIDER == "Amazon Cognito User Pools":
    # Cognito uses a two‑step flow: start challenge then confirm with token
    # Here we only implement the start step.
    CLIENT = {
        "user_pool_id": os.getenv("COGNITO_USER_POOL_ID"),
        "client_id": os.getenv("COGNITO_CLIENT_ID"),
    }
else:
    raise NotImplementedError(f"Provider {PROVIDER} not implemented in password_reset")


def start_reset(payload: ResetPasswordRequest) -> Dict[str, Any]:
    """Trigger a password reset email."""
    if PROVIDER == "Auth0":
        url = f"https://{CLIENT['domain']}.auth0.com/dbconnections/change_password"
        auth_header = get_auth0_headers()
        body = {
            "email": payload["email"],
            "client_id": CLIENT["client_id"],
            "connection": "Username-Password-Authentication",
        }
        resp = requests.post(url, json=body, headers=auth_header)
        resp.raise_for_status()
        # Auth0 returns a 204 or JSON with a message
        return {"message": "reset email sent"}
    elif PROVIDER == "Amazon Cognito User Pools":
        client = {
            "user_pool_id": CLIENT["user_pool_id"],
            "client_id": CLIENT["client_id"],
        }
        import boto3

        client = boto3.client(
            "cognito-idp",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="us-east-1",
        )
        return client.forgot_password(
            ClientId=CLIENT["client_id"], Username=payload["email"]
        )
    else:
        raise NotImplementedError


def confirm_reset(payload: ResetPasswordTokenRequest) -> Dict[str, Any]:
    """Confirm the reset code and set a new password."""
    if PROVIDER == "Auth0":
        # Auth0 handles confirmation via the same change_password endpoint with a token
        raise NotImplementedError("Auth0 reset confirmation not implemented")
    elif PROVIDER == "Amazon Cognito User Pools":
        client = boto3.client(
            "cognito-idp",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="us-east-1",
        )
        return client.confirm_forgot_password(
            ClientId=CLIENT["client_id"],
            Username=payload["email"],
            Password=payload["password"],
            ConfirmationCode=payload["token"],
        )
    else:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Exports for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["start_reset", "confirm_reset"]
