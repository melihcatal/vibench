from __future__ import annotations

from identity_client import (
    load_oauth_config,
    build_auth_url,
    exchange_code_for_tokens,
    fetch_userinfo,
)
from identity_models import (
    AuthorizationRequest,
    TokenResponse,
    NormalizedProfile,
    generate_pkce_pair,
    generate_state,
    generate_nonce,
    normalize_profile_claims,
    AuditEventType,
    build_audit_event,
)


def start_pkce_login(
    redirect_uri: str | None = None,
    connection: str | None = None,
    audience: str | None = None,
    extra_params: dict[str, str] | None = None,
) -> AuthorizationRequest:
    config = load_oauth_config()

    if redirect_uri:
        config.redirect_uri = redirect_uri
    if connection:
        config.connection = connection
    if audience:
        config.audience = audience

    state = generate_state()
    nonce = generate_nonce()
    pkce_pair = generate_pkce_pair()

    auth_url, state, nonce, _ = build_auth_url(
        config=config,
        state=state,
        nonce=nonce,
        pkce_pair=pkce_pair,
        extra_params=extra_params,
    )

    audit_event = build_audit_event(
        event_type=AuditEventType.LOGIN_INITIATED,
        client_id=config.client_id,
        connection=config.connection,
        details={
            "provider": "auth0",
            "domain": config.domain,
            "pkce_enabled": True,
            "challenge_method": pkce_pair.challenge_method,
        },
    )

    return AuthorizationRequest(
        url=auth_url,
        state=state,
        nonce=nonce,
        code_verifier=pkce_pair.code_verifier,
        code_challenge=pkce_pair.code_challenge,
        pkce_enabled=True,
    )


def complete_pkce_login(
    code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    error: str | None = None,
    error_description: str | None = None,
) -> tuple[TokenResponse, NormalizedProfile]:
    if error:
        audit_event = build_audit_event(
            event_type=AuditEventType.CONSENT_DENIED,
            details={
                "provider": "auth0",
                "pkce_enabled": True,
                "error": error,
                "error_description": error_description,
            },
        )
        raise ValueError(f"PKCE login error: {error} - {error_description}")

    if state != expected_state:
        raise ValueError("State mismatch: possible CSRF attack")

    config = load_oauth_config()

    token_data = exchange_code_for_tokens(config, code, code_verifier=code_verifier)

    tokens = TokenResponse(
        access_token=token_data.get("access_token", ""),
        id_token=token_data.get("id_token", ""),
        refresh_token=token_data.get("refresh_token", ""),
        token_type=token_data.get("token_type", "Bearer"),
        expires_in=token_data.get("expires_in", 0),
        scope=token_data.get("scope", ""),
    )

    raw_claims = fetch_userinfo(config, tokens.access_token)

    profile = normalize_profile_claims(
        raw_claims=raw_claims,
        provider="auth0",
        connection=config.connection,
    )

    audit_event = build_audit_event(
        event_type=AuditEventType.TOKEN_EXCHANGED,
        user_sub=profile.sub,
        client_id=config.client_id,
        connection=config.connection,
        details={
            "provider": "auth0",
            "pkce_enabled": True,
            "challenge_method": "S256",
        },
    )

    return tokens, profile


if __name__ == "__main__":
    req = start_pkce_login()
    print(f"PKCE Auth URL: {req.url}")
    print(f"State: {req.state}")
    print(f"Code Verifier: {req.code_verifier}")
    print(f"Code Challenge: {req.code_challenge}")
