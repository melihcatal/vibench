import os
import json
from typing import Optional
from urllib.parse import urlencode

import requests

from identity_client import get_config, IdentityConfig, verify_id_token, validate_state
from identity_models import (
    PKCEState,
    AuthRequest,
    TokenResponse,
    AuditRecord,
    AuditEventType,
)


PROVIDER = "auth0"
AUTH0_AUTHORIZE_ENDPOINT = "https://{domain}/authorize"
AUTH0_TOKEN_ENDPOINT = "https://{domain}/oauth/token"


def generate_pkce_challenge() -> PKCEState:
    return PKCEState()


def start_pkce_login(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    pkce_state = generate_pkce_challenge()
    auth_request = AuthRequest(
        client_id=cfg.auth0_client_id,
        redirect_uri=redirect_uri or cfg.redirect_uri,
        scope=scope or cfg.scope,
        connection=connection or cfg.connection or None,
        audience=audience or cfg.audience or None,
        state=pkce_state.state,
        nonce=pkce_state.nonce,
    )
    params = auth_request.to_query_params()
    params["code_challenge"] = pkce_state.code_challenge()
    params["code_challenge_method"] = "S256"
    authorize_url = AUTH0_AUTHORIZE_ENDPOINT.format(domain=cfg.auth0_domain)
    full_url = f"{authorize_url}?{urlencode(params)}"
    audit_record = AuditRecord(
        event_type=AuditEventType.PKCE_FLOW_STARTED,
        session_id=pkce_state.state,
        provider=PROVIDER,
        details={
            "client_id": cfg.auth0_client_id,
            "redirect_uri": auth_request.redirect_uri,
            "scope": auth_request.scope,
            "code_challenge_method": "S256",
        },
    )
    return {
        "authorization_url": full_url,
        "pkce_state": pkce_state.to_dict(),
        "state": pkce_state.state,
        "nonce": pkce_state.nonce,
        "provider": PROVIDER,
        "auth0_domain": cfg.auth0_domain,
        "audit_record": audit_record.to_dict(),
    }


def complete_pkce_login(
    authorization_code: str,
    state: str,
    pkce_state_data: dict,
    redirect_uri: Optional[str] = None,
    request_headers: Optional[dict] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    pkce_state = PKCEState.from_dict(pkce_state_data)
    if not validate_state(pkce_state.state, state):
        audit_record = AuditRecord(
            event_type=AuditEventType.LOGIN_FAILURE,
            session_id=state,
            provider=PROVIDER,
            success=False,
            error_message="State parameter mismatch in PKCE flow",
        )
        return {
            "success": False,
            "error": "invalid_state",
            "error_description": "State parameter does not match",
            "audit_record": audit_record.to_dict(),
        }
    try:
        token_data = {
            "grant_type": "authorization_code",
            "client_id": cfg.auth0_client_id,
            "code": authorization_code,
            "redirect_uri": redirect_uri or cfg.redirect_uri,
            "code_verifier": pkce_state.code_verifier,
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
        audit_record = AuditRecord(
            event_type=AuditEventType.LOGIN_FAILURE,
            session_id=state,
            provider=PROVIDER,
            success=False,
            error_message=error_detail.get("error_description", str(e)),
        )
        return {
            "success": False,
            "error": error_detail.get("error", "pkce_token_exchange_failed"),
            "error_description": error_detail.get("error_description", str(e)),
            "audit_record": audit_record.to_dict(),
        }
    user_id = None
    id_token_payload = None
    if token_response.id_token:
        try:
            id_token_payload = verify_id_token(
                id_token=token_response.id_token,
                config=cfg,
                nonce=pkce_state.nonce,
            )
            user_id = id_token_payload.get("sub")
        except Exception as e:
            audit_record = AuditRecord(
                event_type=AuditEventType.LOGIN_FAILURE,
                session_id=state,
                provider=PROVIDER,
                success=False,
                error_message=f"ID token verification failed: {str(e)}",
            )
            return {
                "success": False,
                "error": "invalid_id_token",
                "error_description": str(e),
                "audit_record": audit_record.to_dict(),
            }
    audit_record = AuditRecord(
        event_type=AuditEventType.PKCE_FLOW_COMPLETED,
        session_id=state,
        user_id=user_id,
        provider=PROVIDER,
        success=True,
        details={
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
        },
    )
    return {
        "success": True,
        "access_token": token_response.access_token,
        "token_type": token_response.token_type,
        "expires_in": token_response.expires_in,
        "id_token": token_response.id_token,
        "refresh_token": token_response.refresh_token,
        "scope": token_response.scope,
        "user_id": user_id,
        "id_token_payload": id_token_payload,
        "audit_record": audit_record.to_dict(),
    }


def build_pkce_authorization_url(
    client_id: str,
    redirect_uri: str,
    domain: str,
    code_challenge: str,
    state: str,
    scope: str = "openid profile email",
    connection: Optional[str] = None,
    audience: Optional[str] = None,
) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if connection:
        params["connection"] = connection
    if audience:
        params["audience"] = audience
    base_url = f"https://{domain}/authorize"
    return f"{base_url}?{urlencode(params)}"
