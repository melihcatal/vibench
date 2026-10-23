"""
Handle the OAuth/OIDC callback and exchange the authorization code for tokens.
Validates state, exchanges the code via Auth0 /oauth/token, and returns normalized tokens.
"""

import os
import asyncio
from typing import Optional, Dict, Any

from identity_client import create_auth0_client, AUTH0_DOMAIN, AUTH0_CLIENT_ID
from identity_models import TokenResponse, redact_sensitive_fields


class OAuthCallbackError(Exception):
    """Raised when the OAuth callback contains an error."""
    pass


async def handle_oauth_callback(
    code: str,
    state: str,
    expected_state: str,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Process the Auth0 callback after user authorization.

    Validates state, exchanges the authorization code for tokens,
    and returns normalized token response.
    """
    if state != expected_state:
        raise OAuthCallbackError(
            f"State mismatch: expected {expected_state}, got {state}"
        )

    client = create_auth0_client(
        domain=domain or os.getenv("AUTH0_DOMAIN", AUTH0_DOMAIN),
        client_id=client_id or os.getenv("AUTH0_CLIENT_ID", AUTH0_CLIENT_ID),
        client_secret=client_secret or os.getenv("AUTH0_CLIENT_SECRET", ""),
        redirect_uri=redirect_uri or os.getenv("AUTH0_REDIRECT_URI"),
    )

    try:
        token_data = await client.exchange_code(code, code_verifier=code_verifier)
    except Exception as exc:
        raise OAuthCallbackError(f"Token exchange failed: {exc}") from exc

    if "error" in token_data:
        raise OAuthCallbackError(
            f"Auth0 returned error: {token_data.get('error')} - {token_data.get('error_description', '')}"
        )

    tokens = TokenResponse.from_auth0_response(token_data)

    return {
        "tokens": tokens,
        "token_data": redact_sensitive_fields(token_data),
        "provider": "auth0",
        "domain": client.domain,
    }


async def handle_callback_with_session(
    request_params: Dict[str, str],
    session: Dict[str, Any],
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Handle callback using framework request params and session data.

    Extracts code and state from request, validates against session,
    and performs token exchange.
    """
    code = request_params.get("code")
    state = request_params.get("state")
    error = request_params.get("error")

    if error:
        error_desc = request_params.get("error_description", "Unknown error")
        raise OAuthCallbackError(f"Auth0 error: {error} - {error_desc}")

    if not code or not state:
        raise OAuthCallbackError("Missing code or state parameter")

    expected_state = session.get("state")
    redirect_uri = session.get("redirect_uri")

    result = await handle_oauth_callback(
        code=code,
        state=state,
        expected_state=expected_state,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )

    return result


def format_callback_error(error: OAuthCallbackError) -> Dict[str, Any]:
    """Format an OAuth callback error for API response."""
    return {
        "error": True,
        "error_type": "oauth_callback_error",
        "message": str(error),
        "provider": "auth0",
    }


if __name__ == "__main__":
    async def main():
        try:
            result = await handle_oauth_callback(
                code="sample_auth_code",
                state="sample_state",
                expected_state="sample_state",
            )
            print(f"Token exchange successful. Provider: {result['provider']}")
        except OAuthCallbackError as e:
            print(f"Callback error: {e}")

    asyncio.run(main())
