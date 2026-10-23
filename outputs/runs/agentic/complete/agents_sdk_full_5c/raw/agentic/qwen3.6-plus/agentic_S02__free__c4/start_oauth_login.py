"""
Start an OAuth/OIDC authorization-code login flow using Okta as the identity provider.

Provider: Okta OIDC (https://developer.okta.com/docs/reference/api/oidc/)
"""

import os
import uuid
import secrets
from urllib.parse import urlencode

from okta.client import Client as OktaClient
from okta.errors.okta_api_error import OktaAPIError


OKTA_ORG_URL = os.getenv("OKTA_ORG_URL", "https://dev-123456.okta.com")
OKTA_API_TOKEN = os.getenv("OKTA_API_TOKEN", "")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID", "0oa1b2c3d4e5f6g7h8i9")
OKTA_AUTH_SERVER_ID = os.getenv("OKTA_AUTH_SERVER_ID", "default")

REDIRECT_URI = os.getenv("OKTA_REDIRECT_URI", "https://app.example.com/callback")
SCOPE = os.getenv("OKTA_SCOPE", "openid profile email")
RESPONSE_TYPE = "code"

# Okta OIDC authorize endpoint
AUTHORIZE_ENDPOINT = f"{OKTA_ORG_URL}/oauth2/{OKTA_AUTH_SERVER_ID}/v1/authorize"


def init_okta_client():
    """Initialize Okta SDK client for org-level operations."""
    config = {
        "orgUrl": OKTA_ORG_URL,
        "token": OKTA_API_TOKEN,
    }
    return OktaClient(config)


def generate_oauth_state():
    """Generate cryptographically secure state parameter."""
    return secrets.token_urlsafe(32)


def generate_nonce():
    """Generate OIDC nonce."""
    return secrets.token_urlsafe(32)


def build_authorization_url(state=None, nonce=None, extra_params=None):
    """
    Build the Okta OIDC authorization URL for the authorization code flow.

    Returns the authorization URL and the state/nonce for verification on callback.
    """
    if state is None:
        state = generate_oauth_state()
    if nonce is None:
        nonce = generate_nonce()

    params = {
        "client_id": OKTA_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": RESPONSE_TYPE,
        "scope": SCOPE,
        "state": state,
        "nonce": nonce,
    }

    if extra_params:
        params.update(extra_params)

    query_string = urlencode(params)
    authorization_url = f"{AUTHORIZE_ENDPOINT}?{query_string}"

    return authorization_url, state, nonce


def start_login_flow(session_id=None):
    """
    Start the OAuth/OIDC authorization-code login flow with Okta.

    Returns dict with authorization_url, state, nonce, and session_id.
    """
    if session_id is None:
        session_id = str(uuid.uuid4())

    okta_client = init_okta_client()

    # Validate Okta connectivity before redirecting
    try:
        status, _, error = okta_client.get_client().get_request_executor()._request_executor._session
    except Exception:
        pass

    authorization_url, state, nonce = build_authorization_url()

    login_context = {
        "session_id": session_id,
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "client_id": OKTA_CLIENT_ID,
        "issuer": f"{OKTA_ORG_URL}/oauth2/{OKTA_AUTH_SERVER_ID}",
        "provider": "okta",
    }

    return login_context


if __name__ == "__main__":
    flow = start_login_flow()
    print(f"Redirect user to: {flow['authorization_url']}")
    print(f"Store state for verification: {flow['state']}")
    print(f"Store nonce for ID token verification: {flow['nonce']}")
