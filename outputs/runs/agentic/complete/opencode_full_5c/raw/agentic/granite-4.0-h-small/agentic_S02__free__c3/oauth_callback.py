# oauth_callback.py
# SAME-SCENARIO: Handles the OAuth 2.0 / OIDC callback, exchanges the authorization code for tokens, and verifies PKCE code_verifier

import os
import urllib.parse
import json
from typing import Any, Dict

from identity_client import IdentityClient  # local helper
from identity_models import CodeExchangeRequest, TokenResponse  # local helper

# Google‑specific constants (same‑scenario provider)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
TOKEN_URI = "https://oauth2.googleapis.com/token"


def exchange_code_for_tokens(code: str, code_verifier: str) -> TokenResponse:
    """
    Exchange the short‑lived authorization code for access (and optionally refresh) tokens.

    Args:
        code: Authorization code received from the IdP.
        code_verifier: Plain‑text PKCE code_verifier used in the original login.

    Returns: Parsed TokenResponse object containing id_token, access_token, etc.
    """
    body = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }
    response_data = IdentityClient().post(  # concrete Google provider via SDK/client
        url=TOKEN_URI,
        json=body,
    )
    # Provider returns JSON; map to our normalized model
    token_res = TokenResponse(**response_data)
    return token_res


def parse_callback_query(request_query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalise the query parameters delivered to the callback endpoint.

    Args:
        request_query: Dict of GET parameters (e.g., {'code': 'ABC123', 'state': 'XYZ', 'scope': '...'}).

    Returns: Cleaned dict ready for processing.
    """
    # Simple verification – in real code you would also validate nonce, signatures, etc.
    expected = {"code", "state", "scope"}
    if not expected.issubset(request_query):
        raise ValueError("Missing required callback parameters")
    return {k: v for k, v in request_query.items() if k in expected}


# Example handler for a web framework (Flask/Django/etc.)
if __name__ == "__main__":
    # Simulate a request object with a `request.args` dictionary
    fake_query = {
        "code": "AUTH_CODE_987",
        "state": "EXPECTED_STATE_456",
        "scope": "openid email profile",
    }
    params = parse_callback_query(fake_query)
    # Assume we stored the code_verifier in a session; here we use a placeholder
    code_verifier = "PKCE_VERIFIER_789"
    token = exchange_code_for_tokens(params["code"], code_verifier)
    print("Tokens received:", json.dumps(token.dict(), indent=2))
