import os
import time
from identity_models import OAuthConfig, PkcePair, TokenResponse, NormalizedClaims
from identity_client import (
    load_oauth_config,
    generate_pkce_pair,
    build_pkce_authorization_url,
    exchange_code_for_tokens,
    fetch_user_info,
    normalize_claims,
)


def start_pkce_login(
    config: OAuthConfig | None = None,
    state: str | None = None,
    connection: str | None = None,
) -> dict:
    if config is None:
        config = load_oauth_config()

    pkce: PkcePair = generate_pkce_pair()
    authorization_url, generated_state = build_pkce_authorization_url(
        config=config,
        pkce=pkce,
        state=state,
        connection=connection,
    )

    return {
        "authorization_url": authorization_url,
        "state": generated_state,
        "code_verifier": pkce.code_verifier,
        "code_challenge": pkce.code_challenge,
        "code_challenge_method": pkce.code_challenge_method,
        "client_id": config.client_id,
        "domain": config.domain,
        "provider": "auth0",
    }


def complete_pkce_login(
    authorization_code: str,
    code_verifier: str,
    config: OAuthConfig | None = None,
) -> dict:
    if config is None:
        config = load_oauth_config()

    token_response: TokenResponse = exchange_code_for_tokens(
        config=config,
        authorization_code=authorization_code,
        code_verifier=code_verifier,
    )

    if not token_response.is_valid:
        raise ValueError("PKCE token exchange failed")

    profile = fetch_user_info(config=config, access_token=token_response.access_token)
    normalized: NormalizedClaims = normalize_claims(profile, provider="auth0")

    return {
        "access_token": token_response.access_token,
        "id_token": token_response.id_token,
        "refresh_token": token_response.refresh_token,
        "token_type": token_response.token_type,
        "expires_in": token_response.expires_in,
        "user": normalized.to_dict(),
        "provider": "auth0",
        "flow": "pkce",
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def run_pkce_flow(
    authorization_code: str,
    code_verifier: str,
    config: OAuthConfig | None = None,
) -> TokenResponse:
    if config is None:
        config = load_oauth_config()
    return exchange_code_for_tokens(
        config=config,
        authorization_code=authorization_code,
        code_verifier=code_verifier,
    )


if __name__ == "__main__":
    login_session = start_pkce_login()
    print(f"PKCE Authorization URL: {login_session['authorization_url']}")
    print(f"Code Verifier (store securely): {login_session['code_verifier']}")
    print(f"State: {login_session['state']}")
    print(f"Provider: {login_session['provider']}")
