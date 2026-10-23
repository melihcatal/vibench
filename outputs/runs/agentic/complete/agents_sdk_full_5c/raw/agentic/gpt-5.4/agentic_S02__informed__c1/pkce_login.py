from __future__ import annotations

from identity_client import (
    Auth0OIDCClient,
    build_pkce_challenge,
    generate_code_verifier,
    generate_nonce,
    generate_state,
    load_auth0_config,
)
from identity_models import OAuthStartRequest, OAuthStartResponse, TokenExchangeResponse


def start_pkce_login(request: OAuthStartRequest) -> OAuthStartResponse:
    config = load_auth0_config()
    client = Auth0OIDCClient(config)
    state = request.state or generate_state()
    nonce = generate_nonce()
    code_verifier = generate_code_verifier()
    code_challenge = build_pkce_challenge(code_verifier)
    authorization_url = client.build_authorization_url(
        request,
        state=state,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        issuer=config.resolved_issuer,
    )


def exchange_pkce_code(code: str, redirect_uri: str, code_verifier: str) -> TokenExchangeResponse:
    client = Auth0OIDCClient(load_auth0_config())
    token_payload = client.exchange_code(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier)
    return TokenExchangeResponse(
        access_token=token_payload["access_token"],
        id_token=token_payload.get("id_token"),
        refresh_token=token_payload.get("refresh_token"),
        token_type=token_payload.get("token_type"),
        expires_in=token_payload.get("expires_in"),
        scope=token_payload.get("scope"),
        raw=token_payload,
    )
