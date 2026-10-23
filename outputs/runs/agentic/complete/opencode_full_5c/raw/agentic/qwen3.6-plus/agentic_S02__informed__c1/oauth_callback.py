import os
from typing import Optional

from identity_models import OAuthConfig, TokenResponse, UserProfile
from identity_client import (
    load_oauth_config,
    exchange_code_for_tokens,
    fetch_user_info,
    verify_id_token_signature,
    create_auth0_session,
)


def handle_oauth_callback(
    authorization_code: str,
    state: str,
    expected_state: str,
    code_verifier: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> dict:
    if state != expected_state:
        raise ValueError("State mismatch: possible CSRF attack")

    config = load_oauth_config(redirect_uri=redirect_uri)

    token_response = exchange_code_for_tokens(
        config=config,
        authorization_code=authorization_code,
        code_verifier=code_verifier,
    )

    if not token_response.is_valid:
        raise ValueError("Token exchange failed: no access token received")

    is_valid_issuer = verify_id_token_signature(
        id_token=token_response.id_token,
        domain=config.domain,
    )

    user_profile = fetch_user_info(
        config=config,
        access_token=token_response.access_token,
    )

    session = create_auth0_session(
        config=config,
        token_response=token_response,
        user_profile=user_profile,
    )
    session["issuer_verified"] = is_valid_issuer

    return {
        "session": session,
        "user": user_profile.to_dict(),
        "tokens": {
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
            "scope": token_response.scope,
            "has_refresh_token": bool(token_response.refresh_token),
        },
        "provider": "auth0",
        "domain": config.domain,
    }


def process_callback_with_pkce(
    authorization_code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    redirect_uri: Optional[str] = None,
) -> dict:
    return handle_oauth_callback(
        authorization_code=authorization_code,
        state=state,
        expected_state=expected_state,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
    )


def exchange_code_only(
    authorization_code: str,
    state: str,
    expected_state: str,
    code_verifier: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> TokenResponse:
    if state != expected_state:
        raise ValueError("State mismatch: possible CSRF attack")

    config = load_oauth_config(redirect_uri=redirect_uri)

    return exchange_code_for_tokens(
        config=config,
        authorization_code=authorization_code,
        code_verifier=code_verifier,
    )
