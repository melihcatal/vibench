import os
import time
import requests
from typing import Optional, Dict, Any
from identity_models import (
    OAuthConfig,
    TokenResponse,
    TokenExchangeRequest,
    AuditEvent,
    AuditEventType,
    build_audit_event,
)
from identity_client import (
    load_auth0_config,
    validate_state,
    exchange_code_for_tokens,
    parse_callback_url,
)


def handle_oauth_callback(
    callback_url: str,
    expected_state: str,
    config: Optional[OAuthConfig] = None,
    code_verifier: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_auth0_config()

    callback_params = parse_callback_url(callback_url)

    received_state = callback_params.get("state", "")
    if not validate_state(expected_state, received_state):
        audit_event = build_audit_event(
            event_type=AuditEventType.LOGIN_FAILED,
            provider="auth0",
            status="failed",
            details={"error": "state_mismatch", "expected_state": expected_state},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return {
            "success": False,
            "error": "state_mismatch",
            "error_description": "The state parameter does not match",
            "audit_event": audit_event.to_dict(),
        }

    error = callback_params.get("error")
    if error:
        error_description = callback_params.get("error_description", "Unknown error")
        audit_event = build_audit_event(
            event_type=AuditEventType.LOGIN_FAILED,
            provider="auth0",
            status="failed",
            details={
                "error": error,
                "error_description": error_description,
            },
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return {
            "success": False,
            "error": error,
            "error_description": error_description,
            "audit_event": audit_event.to_dict(),
        }

    authorization_code = callback_params.get("code")
    if not authorization_code:
        audit_event = build_audit_event(
            event_type=AuditEventType.LOGIN_FAILED,
            provider="auth0",
            status="failed",
            details={"error": "missing_authorization_code"},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return {
            "success": False,
            "error": "missing_code",
            "error_description": "No authorization code found in callback",
            "audit_event": audit_event.to_dict(),
        }

    try:
        token_response = exchange_code_for_tokens(
            config=config,
            code=authorization_code,
            code_verifier=code_verifier,
        )

        audit_event = build_audit_event(
            event_type=AuditEventType.TOKEN_EXCHANGED,
            provider="auth0",
            status="success",
            details={
                "token_type": token_response.token_type,
                "expires_in": token_response.expires_in,
                "scope": token_response.scope,
                "has_refresh_token": token_response.refresh_token is not None,
                "has_id_token": token_response.id_token is not None,
            },
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return {
            "success": True,
            "token_response": {
                "access_token": token_response.access_token,
                "token_type": token_response.token_type,
                "expires_in": token_response.expires_in,
                "refresh_token": token_response.refresh_token,
                "id_token": token_response.id_token,
                "scope": token_response.scope,
                "issued_at": token_response.issued_at,
            },
            "audit_event": audit_event.to_dict(),
        }

    except requests.exceptions.HTTPError as e:
        error_detail = {}
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = {"error": str(e)}

        audit_event = build_audit_event(
            event_type=AuditEventType.LOGIN_FAILED,
            provider="auth0",
            status="failed",
            details={
                "error": error_detail.get("error", "token_exchange_failed"),
                "error_description": error_detail.get("error_description", str(e)),
            },
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return {
            "success": False,
            "error": error_detail.get("error", "token_exchange_failed"),
            "error_description": error_detail.get("error_description", str(e)),
            "audit_event": audit_event.to_dict(),
        }


def process_auth0_callback(
    callback_url: str,
    expected_state: str,
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    config = load_auth0_config()
    return handle_oauth_callback(
        callback_url=callback_url,
        expected_state=expected_state,
        config=config,
        code_verifier=code_verifier,
    )
