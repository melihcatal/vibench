"""
Handle the OAuth/OIDC callback and exchange authorization code for tokens using Okta.

Provider: Okta OIDC Token Endpoint (https://developer.okta.com/docs/reference/api/oidc/#token)
"""

import os
import base64
import json
import time
import hmac
import hashlib
from urllib.parse import urlencode

import requests
from okta.jwt import JWT as OktaJWT


OKTA_ORG_URL = os.getenv("OKTA_ORG_URL", "https://dev-123456.okta.com")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID", "0oa1b2c3d4e5f6g7h8i9")
OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET", "")
OKTA_AUTH_SERVER_ID = os.getenv("OKTA_AUTH_SERVER_ID", "default")

REDIRECT_URI = os.getenv("OKTA_REDIRECT_URI", "https://app.example.com/callback")

# Okta OIDC token endpoint
TOKEN_ENDPOINT = f"{OKTA_ORG_URL}/oauth2/{OKTA_AUTH_SERVER_ID}/v1/token"
# Okta JWKS endpoint for ID token verification
JWKS_URI = f"{OKTA_ORG_URL}/oauth2/{OKTA_AUTH_SERVER_ID}/v1/keys"


class OktaCallbackError(Exception):
    """Raised when Okta callback processing fails."""
    pass


def verify_state(received_state: str, expected_state: str) -> bool:
    """Verify OAuth state parameter to prevent CSRF."""
    if not received_state or not expected_state:
        return False
    return hmac.compare_digest(received_state, expected_state)


def exchange_authorization_code(
    authorization_code: str,
    code_verifier: str = None,
    expected_state: str = None,
    received_state: str = None,
) -> dict:
    """
    Exchange Okta authorization code for tokens (access_token, id_token, refresh_token).

    Uses the Okta /oauth2/{authServerId}/v1/token endpoint.
    """
    if expected_state and received_state:
        if not verify_state(received_state, expected_state):
            raise OktaCallbackError("State parameter mismatch - possible CSRF attack")

    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": OKTA_CLIENT_ID,
        "client_secret": OKTA_CLIENT_SECRET,
    }

    if code_verifier:
        token_data["code_verifier"] = code_verifier

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        TOKEN_ENDPOINT,
        data=urlencode(token_data),
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:
        raise OktaCallbackError(
            f"Okta token exchange failed: {response.status_code} - {response.text}"
        )

    token_response = response.json()
    return token_response


def verify_okta_id_token(id_token: str, expected_nonce: str = None) -> dict:
    """
    Verify Okta ID token using Okta's JWKS endpoint.

    Validates signature, issuer, audience, expiration, and nonce.
    """
    jwks = requests.get(JWKS_URI, timeout=15).json()

    # Use Okta's JWT library for verification
    verifier = OktaJWT(JWKS_URI)
    claims = verifier.get_claims(id_token, OKTA_CLIENT_ID)

    if expected_nonce:
        token_nonce = claims.get("nonce")
        if not hmac.compare_digest(str(token_nonce), str(expected_nonce)):
            raise OktaCallbackError("Nonce mismatch - possible replay attack")

    return claims


def handle_callback(
    authorization_code: str,
    state: str = None,
    nonce: str = None,
    code_verifier: str = None,
) -> dict:
    """
    Full Okta callback handler: exchange code, verify tokens, return user session.
    """
    token_response = exchange_authorization_code(
        authorization_code=authorization_code,
        code_verifier=code_verifier,
        received_state=state,
        expected_state=state,
    )

    id_token = token_response.get("id_token")
    if id_token:
        claims = verify_okta_id_token(id_token, expected_nonce=nonce)
    else:
        claims = {}

    session_data = {
        "access_token": token_response.get("access_token"),
        "token_type": token_response.get("token_type", "Bearer"),
        "expires_in": token_response.get("expires_in", 3600),
        "refresh_token": token_response.get("refresh_token"),
        "id_token": id_token,
        "claims": claims,
        "provider": "okta",
        "authenticated_at": int(time.time()),
    }

    return session_data


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        auth_code = sys.argv[1]
        session = handle_callback(auth_code)
        print(json.dumps(session, indent=2))
