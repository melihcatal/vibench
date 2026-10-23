"""Handle the callback and exchange an authorization code for tokens using Google Identity Platform."""

import os
import time
from typing import Optional, Dict, Any

import requests

from identity_client import IdentityClient, GoogleOIDCConfig
from identity_models import TokenExchangeRequest, TokenResponse


def exchange_code_for_tokens(
    code: str,
    code_verifier: Optional[str] = None,
    state: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> TokenResponse:
    """
    Exchange an OAuth authorization code for access/ID tokens
    via Google Identity Platform's token endpoint.
    """
    token_request = TokenExchangeRequest(
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        code_verifier=code_verifier,
    )

    body = token_request.to_form_body()

    response = requests.post(
        GoogleOIDCConfig.TOKEN_ENDPOINT,
        data=body,
        headers={"Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    token_data = response.json()

    return TokenResponse.from_dict(token_data)


def validate_state(expected_state: Optional[str], received_state: Optional[str]) -> bool:
    """Validate the OAuth state parameter to prevent CSRF."""
    if expected_state is None or received_state is None:
        return False
    return expected_state == received_state


def handle_oauth_callback(
    authorization_code: str,
    state_received: Optional[str] = None,
    state_expected: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Full callback handler: validate state, exchange code for tokens,
    and return a structured result.
    """
    if state_expected and state_received:
        if not validate_state(state_expected, state_received):
            return {
                "error": "state_mismatch",
                "message": "OAuth state parameter validation failed",
                "provider": GoogleOIDCConfig.PROVIDER_NAME,
            }

    try:
        token_response = exchange_code_for_tokens(
            code=authorization_code,
            code_verifier=code_verifier,
        )
        return {
            "success": True,
            "token_response": {
                "token_type": token_response.token_type,
                "expires_in": token_response.expires_in,
                "scope": token_response.scope,
                "has_id_token": token_response.id_token is not None,
                "has_refresh_token": token_response.refresh_token is not None,
            },
            "provider": GoogleOIDCConfig.PROVIDER_NAME,
            "timestamp": time.time(),
        }
    except requests.RequestException as exc:
        return {
            "success": False,
            "error": "token_exchange_failed",
            "message": str(exc),
            "provider": GoogleOIDCConfig.PROVIDER_NAME,
        }


if __name__ == "__main__":
    demo_code = os.environ.get("DEMO_AUTH_CODE", "")
    if demo_code:
        result = handle_oauth_callback(demo_code)
        print("Callback result:", result)
    else:
        print("Set DEMO_AUTH_CODE env var to test callback handling.")
