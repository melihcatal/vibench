from __future__ import annotations

from identity_client import load_oauth_config, exchange_code_for_tokens
from identity_models import (
    CallbackPayload,
    TokenResponse,
    AuditEventType,
    build_audit_event,
)


def handle_oauth_callback(
    code: str,
    state: str,
    expected_state: str,
    error: str | None = None,
    error_description: str | None = None,
) -> TokenResponse:
    callback = CallbackPayload(
        code=code,
        state=state,
        error=error or "",
        error_description=error_description or "",
    )

    if callback.error:
        audit_event = build_audit_event(
            event_type=AuditEventType.CONSENT_DENIED,
            details={
                "provider": "auth0",
                "error": callback.error,
                "error_description": callback.error_description,
            },
        )
        raise ValueError(
            f"OAuth callback error: {callback.error} - {callback.error_description}"
        )

    if callback.state != expected_state:
        raise ValueError("State mismatch: possible CSRF attack")

    config = load_oauth_config()

    token_data = exchange_code_for_tokens(config, callback.code)

    audit_event = build_audit_event(
        event_type=AuditEventType.TOKEN_EXCHANGED,
        client_id=config.client_id,
        details={
            "provider": "auth0",
            "domain": config.domain,
            "token_type": token_data.get("token_type", ""),
            "scope": token_data.get("scope", ""),
            "expires_in": token_data.get("expires_in", 0),
        },
    )

    return TokenResponse(
        access_token=token_data.get("access_token", ""),
        id_token=token_data.get("id_token", ""),
        refresh_token=token_data.get("refresh_token", ""),
        token_type=token_data.get("token_type", "Bearer"),
        expires_in=token_data.get("expires_in", 0),
        scope=token_data.get("scope", ""),
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4:
        tokens = handle_oauth_callback(sys.argv[1], sys.argv[2], sys.argv[3])
        print(f"Access token received (length={len(tokens.access_token)})")
    else:
        print("Usage: python oauth_callback.py <code> <state> <expected_state>")
