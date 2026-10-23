"""
Handle the OAuth/OIDC callback and exchange an authorization code for tokens
using Auth0.

Receives the callback request at the redirect_uri, validates the state
parameter, and exchanges the authorization code for access, ID, and
optionally refresh tokens via the Auth0 /oauth/token endpoint.
"""

import os
from typing import Any, Dict, Optional

from identity_models import (
    TokenResponse,
    extract_id_token_claims,
    parse_callback_query,
)
from identity_client import (
    IdentityClient,
    AUTH0_TOKEN_URL,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_REDIRECT_URI,
)


class CallbackError(Exception):
    """Raised when the OAuth callback contains an error or fails validation."""
    pass


def validate_state(expected_state: str, received_state: Optional[str]) -> None:
    """
    Validate the OAuth state parameter to prevent CSRF attacks.

    The state received from Auth0's callback must match the one
    generated when the login was initiated.
    """
    if not received_state:
        raise CallbackError("Missing state parameter in callback")
    if received_state != expected_state:
        raise CallbackError("State mismatch: possible CSRF attack")


def handle_oauth_callback(
    query_params: Dict[str, str],
    expected_state: str,
    code_verifier: Optional[str] = None,
    client: Optional[IdentityClient] = None,
) -> TokenResponse:
    """
    Process the Auth0 OAuth callback and exchange the authorization code
    for tokens.

    Steps:
    1. Parse callback query parameters (code, state, error).
    2. Validate the state parameter against the expected value.
    3. Check for error responses from Auth0.
    4. Exchange the authorization code at Auth0 /oauth/token endpoint.
    5. Build and return a TokenResponse.

    Args:
        query_params: Query string parameters from the callback URL.
        expected_state: The state value generated at login initiation.
        code_verifier: Optional PKCE code verifier if PKCE was used.
        client: Optional IdentityClient instance (Auth0 tenant config).

    Returns:
        TokenResponse containing access_token, id_token, etc.

    Raises:
        CallbackError: If the callback contains an error or state mismatch.
    """
    parsed = parse_callback_query(query_params)

    if parsed["error"]:
        raise CallbackError(
            f"Auth0 callback error: {parsed['error']} - "
            f"{parsed.get('error_description', 'No description')}"
        )

    validate_state(expected_state, parsed["state"])

    code = parsed["code"]
    if not code:
        raise CallbackError("Missing authorization code in callback")

    if client is None:
        client = IdentityClient()

    try:
        token_data = client.exchange_authorization_code(
            code=code,
            code_verifier=code_verifier,
        )
    except Exception as exc:
        raise CallbackError(f"Token exchange failed: {exc}") from exc

    id_token_claims = {}
    id_token_raw = token_data.get("id_token")
    if id_token_raw:
        id_token_claims = extract_id_token_claims(id_token_raw)

    response = TokenResponse(
        access_token=token_data["access_token"],
        token_type=token_data.get("token_type", "Bearer"),
        expires_in=token_data.get("expires_in", 3600),
        id_token=id_token_raw,
        refresh_token=token_data.get("refresh_token"),
        scope=token_data.get("scope"),
        raw_response=token_data,
    )

    return response


def handle_oidc_callback_with_nonce_validation(
    query_params: Dict[str, str],
    expected_state: str,
    expected_nonce: str,
    client: Optional[IdentityClient] = None,
) -> TokenResponse:
    """
    Handle an Auth0 OIDC callback with nonce validation.

    In addition to state validation, this verifies that the nonce claim
    in the ID token matches the expected nonce generated at login start.
    """
    token_response = handle_oauth_callback(
        query_params=query_params,
        expected_state=expected_state,
        client=client,
    )

    if token_response.id_token:
        claims = extract_id_token_claims(token_response.id_token)
        received_nonce = claims.get("nonce")
        if received_nonce != expected_nonce:
            raise CallbackError(
                "Nonce mismatch: the ID token nonce does not match "
                "the expected nonce. Possible replay attack."
            )

    return token_response


def refresh_tokens(
    refresh_token: str,
    client: Optional[IdentityClient] = None,
) -> TokenResponse:
    """
    Refresh expired tokens using an Auth0 refresh token.

    Auth0 issues refresh tokens when the offline_access scope is
    requested and the application is configured to allow refresh token
    rotation in the Auth0 dashboard.
    """
    if client is None:
        client = IdentityClient()

    token_data = client.refresh_token(refresh_token)

    return TokenResponse(
        access_token=token_data["access_token"],
        token_type=token_data.get("token_type", "Bearer"),
        expires_in=token_data.get("expires_in", 3600),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token", refresh_token),
        scope=token_data.get("scope"),
        raw_response=token_data,
    )


def revoke_and_logout(
    access_token: str,
    refresh_token: Optional[str] = None,
    client: Optional[IdentityClient] = None,
    return_to: Optional[str] = None,
) -> str:
    """
    Revoke tokens and build an Auth0 logout URL.

    Calls the Auth0 /oauth/revoke endpoint to invalidate tokens and
    then constructs the Auth0 /v2/logout URL for browser-side session
    termination.
    """
    if client is None:
        client = IdentityClient()

    if refresh_token:
        client.revoke_token(refresh_token)
    client.revoke_token(access_token)

    logout_url = client.build_logout_url(return_to=return_to)
    return logout_url


if __name__ == "__main__":
    sample_callback = {
        "code": "auth0_sample_code_abc123",
        "state": "sample_state_xyz",
    }
    print("Auth0 callback handler ready.")
    print(f"Token endpoint: {AUTH0_TOKEN_URL}")
