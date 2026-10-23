from __future__ import annotations

from identity_client import (
    Auth0OIDCClient,
    generate_code_verifier,
    generate_nonce,
    generate_pkce_challenge,
    generate_state,
)
from identity_models import OAuthStartRequest, OAuthStartResponse, TokenExchangeResult


def start_pkce_login(request: OAuthStartRequest) -> OAuthStartResponse:
    client = Auth0OIDCClient()
    state = request.state or generate_state()
    nonce = generate_nonce()
    code_verifier = generate_code_verifier()
    code_challenge = generate_pkce_challenge(code_verifier)
    authorization_url = client.build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        state=state,
        nonce=nonce,
        audience=request.audience,
        prompt=request.prompt,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )


def complete_pkce_callback(code: str, redirect_uri: str, code_verifier: str) -> TokenExchangeResult:
    client = Auth0OIDCClient()
    token_payload = client.exchange_code(
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    return TokenExchangeResult(
        access_token=str(token_payload["access_token"]),
        id_token=token_payload.get("id_token"),
        refresh_token=token_payload.get("refresh_token"),
        token_type=str(token_payload.get("token_type", "Bearer")),
        expires_in=token_payload.get("expires_in"),
        scope=token_payload.get("scope"),
        raw=token_payload,
    )
