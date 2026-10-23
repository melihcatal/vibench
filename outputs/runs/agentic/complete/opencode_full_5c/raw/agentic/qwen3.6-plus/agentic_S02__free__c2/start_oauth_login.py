from __future__ import annotations

from identity_client import load_oauth_config, build_auth_url
from identity_models import (
    AuthorizationRequest,
    AuditEventType,
    build_audit_event,
    generate_state,
    generate_nonce,
)


def start_oauth_login(
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

    auth_url, state, nonce, _ = build_auth_url(
        config=config,
        state=state,
        nonce=nonce,
        extra_params=extra_params,
    )

    audit_event = build_audit_event(
        event_type=AuditEventType.LOGIN_INITIATED,
        client_id=config.client_id,
        connection=config.connection,
        details={
            "provider": "auth0",
            "domain": config.domain,
            "redirect_uri": config.redirect_uri,
            "scope": config.scope,
        },
    )

    return AuthorizationRequest(
        url=auth_url,
        state=state,
        nonce=nonce,
        pkce_enabled=False,
    )


if __name__ == "__main__":
    req = start_oauth_login()
    print(f"Auth URL: {req.url}")
    print(f"State: {req.state}")
    print(f"Nonce: {req.nonce}")
