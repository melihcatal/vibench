import os
import uuid
import requests
from typing import Optional, Dict, Any
from identity_models import (
    OAuthConfig,
    AuthorizationRequest,
    AuditEvent,
    AuditEventType,
    build_audit_event,
)
from identity_client import load_auth0_config, build_authorization_url


def start_oauth_login(
    config: Optional[OAuthConfig] = None,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    connection: Optional[str] = None,
    prompt: Optional[str] = None,
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

    auth_request = AuthorizationRequest(
        client_id=config.client_id,
        redirect_uri=config.redirect_uri,
        scope=config.scope,
        response_type=config.response_type,
        state=config.state,
        nonce=config.nonce,
        audience=config.audience,
        connection=config.connection,
        prompt=prompt,
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
            "authorization_endpoint": config.authorization_endpoint,
            "client_id": config.client_id,
            "scope": config.scope,
            "state": config.state,
            "nonce": config.nonce,
            "session_id": session_id,
        },
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return {
        "authorization_url": authorization_url,
        "state": config.state,
        "nonce": config.nonce,
        "session_id": session_id,
        "client_id": config.client_id,
        "provider": "auth0",
        "auth0_domain": os.environ.get("AUTH0_DOMAIN", ""),
        "audit_event": audit_event.to_dict(),
    }


def initiate_auth0_login(
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile email",
    connection: Optional[str] = None,
    audience: Optional[str] = None,
    prompt: Optional[str] = None,
) -> Dict[str, Any]:
    config = load_auth0_config()
    if redirect_uri:
        config.redirect_uri = redirect_uri
    if scope:
        config.scope = scope
    if connection:
        config.connection = connection
    if audience:
        config.audience = audience

    return start_oauth_login(
        config=config,
        redirect_uri=config.redirect_uri,
        scope=config.scope,
        connection=connection,
        prompt=prompt,
    )
