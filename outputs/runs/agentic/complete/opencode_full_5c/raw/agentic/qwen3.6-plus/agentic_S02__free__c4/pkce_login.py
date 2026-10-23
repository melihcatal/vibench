import os
import uuid
import requests
from typing import Optional, Dict, Any, Tuple
from identity_models import (
    OAuthConfig,
    PKCEConfig,
    TokenResponse,
    AuthorizationRequest,
    AuditEvent,
    AuditEventType,
    build_audit_event,
)
from identity_client import (
    load_auth0_config,
    generate_pkce_pair,
    exchange_code_for_tokens,
    parse_callback_url,
    validate_state,
)


def start_pkce_login(
    config: Optional[OAuthConfig] = None,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    connection: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_auth0_config()

    if redirect_uri:
        config.redirect_uri = redirect_uri
    if scope:
        config.scope = scope
    if connection:
        config.connection = connection

    code_verifier, code_challenge = generate_pkce_pair()

    pkce_config = PKCEConfig(
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    auth_request = AuthorizationRequest(
        client_id=config.client_id,
        redirect_uri=config.redirect_uri,
        scope=config.scope,
        response_type="code",
        state=config.state,
        nonce=config.nonce,
        code_challenge=pkce_config.code_challenge,
        code_challenge_method=pkce_config.code_challenge_method,
        audience=config.audience,
        connection=config.connection,
    )

    params = auth_request.to_params()
    query_string = "&".join(
        f"{k}={requests.utils.quote(str(v))}" for k, v in params.items()
    )
    authorization_url = f"{config.authorization_endpoint}?{query_string}"

    session_id = str(uuid.uuid4())
    audit_event = build_audit_event(
        event_type=AuditEventType.LOGIN_INITIATED,
        provider="auth0",
        status="initiated",
        details={
            "flow_type": "pkce",
            "authorization_endpoint": config.authorization_endpoint,
            "client_id": config.client_id,
            "scope": config.scope,
            "code_challenge_method": pkce_config.code_challenge_method,
            "session_id": session_id,
        },
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return {
        "authorization_url": authorization_url,
        "state": config.state,
        "nonce": config.nonce,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "session_id": session_id,
        "client_id": config.client_id,
        "provider": "auth0",
        "auth0_domain": os.environ.get("AUTH0_DOMAIN", ""),
        "audit_event": audit_event.to_dict(),
    }


def complete_pkce_login(
    callback_url: str,
    expected_state: str,
    code_verifier: str,
    config: Optional[OAuthConfig] = None,
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
            details={"error": "state_mismatch", "flow_type": "pkce"},
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
                "flow_type": "pkce",
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
            details={"error": "missing_authorization_code", "flow_type": "pkce"},
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
                "flow_type": "pkce",
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
                "flow_type": "pkce",
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


def initiate_auth0_pkce_login(
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile email",
    connection: Optional[str] = None,
) -> Dict[str, Any]:
    config = load_auth0_config()
    return start_pkce_login(
        config=config,
        redirect_uri=redirect_uri or config.redirect_uri,
        scope=scope,
        connection=connection,
    )
