"""
[SAME-SCENARIO] Starts an OAuth/OIDC authorization-code login flow using Auth0.

Constructs the authorization URL for the Auth0 Authentication API
(https://AUTH0_DOMAIN/authorize) and records a login-start audit event.
Uses AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables.
"""

import urllib.parse
from typing import List, Optional, Tuple

from identity_client import Auth0Config, get_state_store, get_audit_logger, load_config
from identity_models import OAuthState, AuditEvent


def build_authorization_url(
    config: Optional[Auth0Config] = None,
    redirect_uri: Optional[str] = None,
    extra_scopes: Optional[List[str]] = None,
    connection: Optional[str] = None,
    prompt: Optional[str] = None,
    max_age: Optional[int] = None,
) -> Tuple[str, OAuthState]:
    """
    Build the Auth0 authorization endpoint URL for an authorization-code flow.

    Auth0 Authentication API endpoint:
        https://{AUTH0_DOMAIN}/authorize

    Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID
    """
    if config is None:
        config = load_config()

    state_obj = OAuthState(
        redirect_uri=redirect_uri or config.redirect_uri,
        scopes=config.build_scopes(extra_scopes),
    )
    state_store = get_state_store()
    state_store.store(state_obj)

    params: dict = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": state_obj.redirect_uri,
        "scope": state_obj.scopes,
        "state": state_obj.state,
        "nonce": state_obj.nonce,
    }

    if connection:
        params["connection"] = connection
    if prompt:
        params["prompt"] = prompt
    if max_age is not None:
        params["max_age"] = str(max_age)

    auth_url = f"https://{config.domain}/authorize?{urllib.parse.urlencode(params)}"

    # Log the login start event
    audit_logger = get_audit_logger()
    audit_logger.log(
        AuditEvent(
            event_type="login_start",
            provider="auth0",
            state=state_obj.state,
            details={
                "domain": config.domain,
                "client_id": config.client_id,
                "redirect_uri": state_obj.redirect_uri,
                "scopes": state_obj.scopes,
                "connection": connection or "",
            },
        )
    )

    return auth_url, state_obj


def start_login(
    redirect_uri: Optional[str] = None,
    extra_scopes: Optional[List[str]] = None,
    connection: Optional[str] = None,
) -> dict:
    """
    Entry point: start a federated login and return the authorization URL
    along with the OAuth state tracking information.
    """
    config = load_config()
    auth_url, state_obj = build_authorization_url(
        config=config,
        redirect_uri=redirect_uri,
        extra_scopes=extra_scopes,
        connection=connection,
    )

    return {
        "authorization_url": auth_url,
        "state": state_obj.state,
        "nonce": state_obj.nonce,
        "provider": "auth0",
        "issuer": config.issuer,
        "domain": config.domain,
    }
