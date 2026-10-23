import os
import json
import uuid
from typing import Optional
from urllib.parse import urlencode

import requests

from identity_client import get_config, IdentityConfig
from identity_models import AuthRequest, AuditRecord, AuditEventType


PROVIDER = "auth0"
AUTH0_AUTHORIZE_ENDPOINT = "https://{domain}/authorize"


def start_oauth_login(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
    prompt: Optional[str] = None,
    max_age: Optional[int] = None,
    extra_params: Optional[dict] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    session_id = str(uuid.uuid4())
    auth_request = AuthRequest(
        client_id=cfg.auth0_client_id,
        redirect_uri=redirect_uri or cfg.redirect_uri,
        scope=scope or cfg.scope,
        connection=connection or cfg.connection or None,
        audience=audience or cfg.audience or None,
        prompt=prompt,
        max_age=max_age,
    )
    params = auth_request.to_query_params()
    if extra_params:
        params.update(extra_params)
    authorize_url = AUTH0_AUTHORIZE_ENDPOINT.format(domain=cfg.auth0_domain)
    full_url = f"{authorize_url}?{urlencode(params)}"
    audit_record = AuditRecord(
        event_type=AuditEventType.LOGIN_INITIATED,
        session_id=session_id,
        provider=PROVIDER,
        details={
            "client_id": cfg.auth0_client_id,
            "redirect_uri": auth_request.redirect_uri,
            "scope": auth_request.scope,
            "state": auth_request.state,
        },
    )
    return {
        "authorization_url": full_url,
        "state": auth_request.state,
        "nonce": auth_request.nonce,
        "session_id": session_id,
        "provider": PROVIDER,
        "auth0_domain": cfg.auth0_domain,
        "audit_record": audit_record.to_dict(),
    }


def build_auth0_login_url(
    client_id: str,
    redirect_uri: str,
    domain: str,
    scope: str = "openid profile email",
    response_type: str = "code",
    connection: Optional[str] = None,
    audience: Optional[str] = None,
) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": response_type,
        "scope": scope,
        "state": str(uuid.uuid4()),
        "nonce": str(uuid.uuid4()),
    }
    if connection:
        params["connection"] = connection
    if audience:
        params["audience"] = audience
    base_url = f"https://{domain}/authorize"
    return f"{base_url}?{urlencode(params)}"


def initiate_sso_redirect(
    connection: str,
    redirect_uri: Optional[str] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    return start_oauth_login(
        redirect_uri=redirect_uri,
        connection=connection,
        prompt="login",
        config=config,
    )


def initiate_mfa_login(
    redirect_uri: Optional[str] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    return start_oauth_login(
        redirect_uri=redirect_uri,
        prompt="consent",
        acr_values="urn:mfa",
        config=config,
    )
