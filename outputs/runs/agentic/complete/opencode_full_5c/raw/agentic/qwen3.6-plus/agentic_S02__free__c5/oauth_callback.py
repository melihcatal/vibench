import os
from typing import Optional

import requests

from identity_client import (
    get_config,
    IdentityConfig,
    exchange_code_for_tokens,
    verify_id_token,
    validate_state,
    extract_ip_address,
    extract_user_agent,
)
from identity_models import TokenResponse, AuditRecord, AuditEventType


PROVIDER = "auth0"
AUTH0_TOKEN_ENDPOINT = "https://{domain}/oauth/token"


def handle_oauth_callback(
    authorization_code: str,
    state: str,
    expected_state: str,
    redirect_uri: Optional[str] = None,
    session_id: Optional[str] = None,
    request_headers: Optional[dict] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    if not validate_state(expected_state, state):
        audit_record = AuditRecord(
            event_type=AuditEventType.LOGIN_FAILURE,
            session_id=session_id,
            provider=PROVIDER,
            success=False,
            error_message="State parameter mismatch - possible CSRF attack",
            ip_address=extract_ip_address(request_headers or {}),
            user_agent=extract_user_agent(request_headers or {}),
        )
        return {
            "success": False,
            "error": "invalid_state",
            "error_description": "State parameter does not match expected value",
            "audit_record": audit_record.to_dict(),
        }
    try:
        token_response = exchange_code_for_tokens(
            authorization_code=authorization_code,
            redirect_uri=redirect_uri,
            config=cfg,
        )
    except requests.HTTPError as e:
        error_detail = e.response.json() if e.response is not None else {}
        audit_record = AuditRecord(
            event_type=AuditEventType.LOGIN_FAILURE,
            session_id=session_id,
            provider=PROVIDER,
            success=False,
            error_message=error_detail.get("error_description", str(e)),
            ip_address=extract_ip_address(request_headers or {}),
            user_agent=extract_user_agent(request_headers or {}),
        )
        return {
            "success": False,
            "error": error_detail.get("error", "token_exchange_failed"),
            "error_description": error_detail.get("error_description", str(e)),
            "audit_record": audit_record.to_dict(),
        }
    id_token_payload = None
    if token_response.id_token:
        try:
            id_token_payload = verify_id_token(
                id_token=token_response.id_token,
                config=cfg,
            )
        except Exception as e:
            audit_record = AuditRecord(
                event_type=AuditEventType.LOGIN_FAILURE,
                session_id=session_id,
                provider=PROVIDER,
                success=False,
                error_message=f"ID token verification failed: {str(e)}",
                ip_address=extract_ip_address(request_headers or {}),
                user_agent=extract_user_agent(request_headers or {}),
            )
            return {
                "success": False,
                "error": "invalid_id_token",
                "error_description": str(e),
                "audit_record": audit_record.to_dict(),
            }
    user_id = id_token_payload.get("sub") if id_token_payload else None
    audit_record = AuditRecord(
        event_type=AuditEventType.LOGIN_SUCCESS,
        session_id=session_id,
        user_id=user_id,
        provider=PROVIDER,
        details={
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
            "scope": token_response.scope,
        },
        ip_address=extract_ip_address(request_headers or {}),
        user_agent=extract_user_agent(request_headers or {}),
    )
    return {
        "success": True,
        "access_token": token_response.access_token,
        "token_type": token_response.token_type,
        "expires_in": token_response.expires_in,
        "id_token": token_response.id_token,
        "refresh_token": token_response.refresh_token,
        "scope": token_response.scope,
        "id_token_payload": id_token_payload,
        "user_id": user_id,
        "audit_record": audit_record.to_dict(),
    }


def process_callback_with_pkce(
    authorization_code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    redirect_uri: Optional[str] = None,
    session_id: Optional[str] = None,
    request_headers: Optional[dict] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    if not validate_state(expected_state, state):
        audit_record = AuditRecord(
            event_type=AuditEventType.LOGIN_FAILURE,
            session_id=session_id,
            provider=PROVIDER,
            success=False,
            error_message="State parameter mismatch in PKCE flow",
        )
        return {
            "success": False,
            "error": "invalid_state",
            "audit_record": audit_record.to_dict(),
        }
    try:
        token_data = {
            "grant_type": "authorization_code",
            "client_id": cfg.auth0_client_id,
            "code": authorization_code,
            "redirect_uri": redirect_uri or cfg.redirect_uri,
            "code_verifier": code_verifier,
        }
        response = requests.post(
            AUTH0_TOKEN_ENDPOINT.format(domain=cfg.auth0_domain),
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        response.raise_for_status()
        token_response = TokenResponse.from_dict(response.json())
    except requests.HTTPError as e:
        error_detail = e.response.json() if e.response is not None else {}
        return {
            "success": False,
            "error": error_detail.get("error", "pkce_token_exchange_failed"),
            "error_description": error_detail.get("error_description", str(e)),
        }
    user_id = None
    if token_response.id_token:
        try:
            id_token_payload = verify_id_token(
                id_token=token_response.id_token,
                config=cfg,
            )
            user_id = id_token_payload.get("sub")
        except Exception:
            pass
    audit_record = AuditRecord(
        event_type=AuditEventType.PKCE_FLOW_COMPLETED,
        session_id=session_id,
        user_id=user_id,
        provider=PROVIDER,
        success=True,
    )
    return {
        "success": True,
        "access_token": token_response.access_token,
        "token_type": token_response.token_type,
        "expires_in": token_response.expires_in,
        "id_token": token_response.id_token,
        "refresh_token": token_response.refresh_token,
        "user_id": user_id,
        "audit_record": audit_record.to_dict(),
    }
