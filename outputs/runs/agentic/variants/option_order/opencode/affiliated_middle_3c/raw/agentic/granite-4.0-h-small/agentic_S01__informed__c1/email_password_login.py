# email_password_login.py
# Signs in a user with email and password and returns tokens (same‑scenario implementation)

import os
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Import local helpers
# ---------------------------------------------------------------------------
from identity_client import (
    PROVIDER,
    get_auth0_headers,
    get_cognito_admin_client,
)
from identity_models import (
    EmailPasswordLoginRequest,
    RefreshTokenRequest,
    standardize_login_response,
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
    CLIENT = get_cognito_admin_client()
else:
    raise NotImplementedError(
        f"Provider {PROVIDER} not implemented in email_password_login"
    )


def login(payload: EmailPasswordLoginRequest) -> Dict[str, Any]:
    """Authenticate with email/password and return a token set."""
    if PROVIDER == "Auth0":
        url = f"https://{CLIENT['domain']}.auth0.com/oauth/token"
        auth_header = get_auth0_headers()
        body = {
            "grant_type": "password",
            "username": payload["email"],
            "password": payload["password"],
            "scope": "openid profile email",
            "client_id": CLIENT["client_id"],
            "client_secret": CLIENT["client_secret"],
        }
        resp = requests.post(url, data=body, headers=auth_header)
        resp.raise_for_status()
        data = resp.json()
        return standardize_login_response(data)
    elif PROVIDER == "Amazon Cognito User Pools":
        client = CLIENT
        resp = client.admin_initiate_auth(
            UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
            ClientId=os.getenv("COGNITO_CLIENT_ID"),
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": payload["email"],
                "PASSWORD": payload["password"],
            },
        )
        # Cognito returns AccessToken, RefreshToken, ExpiresIn, TokenType
        return {
            "access_token": resp["AuthenticationResult"]["AccessToken"],
            "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
            "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
            "token_type": resp["AuthenticationResult"]["TokenType"],
        }
    else:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Refresh flow (shared between providers for later steps)
# ---------------------------------------------------------------------------


def refresh(payload: RefreshTokenRequest) -> Dict[str, Any]:
    """Refresh an access token using a refresh token."""
    if PROVIDER == "Auth0":
        url = f"https://{CLIENT['domain']}.auth0.com/oauth/token"
        auth_header = get_auth0_headers()
        body = {
            "grant_type": "refresh_token",
            "refresh_token": payload["refresh_token"],
            "client_id": CLIENT["client_id"],
            "client_secret": CLIENT["client_secret"],
        }
        resp = requests.post(url, json=body, headers=auth_header)
        resp.raise_for_status()
        data = resp.json()
        return standardize_login_response(data)
    elif PROVIDER == "Amazon Cognito User Pools":
        client = CLIENT
        resp = client.admin_initiate_auth(
            UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
            ClientId=os.getenv("COGNITO_CLIENT_ID"),
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": payload["refresh_token"]},
        )
        return {
            "access_token": resp["AuthenticationResult"]["AccessToken"],
            "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
            "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
            "token_type": resp["AuthenticationResult"]["TokenType"],
        }
    else:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Exports for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["login", "refresh"]
