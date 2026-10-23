import secrets
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import (
    OAuthConfig,
    AuthRequest,
    generate_state,
    generate_nonce,
)
from identity_client import load_oauth_config, extract_provider_from_issuer


AUTH0_DOMAIN = "dev-example.auth0.com"
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}"
AUTH0_AUTHORIZE_URL = f"{AUTH0_ISSUER}/authorize"


def start_auth0_login(
    config: Optional[OAuthConfig] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
    prompt: Optional[str] = None,
    login_hint: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_oauth_config()

    state = generate_state()
    nonce = generate_nonce()
    scope_list = scopes if scopes is not None else config.scopes

    auth_request = AuthRequest(
        client_id=config.client_id,
        redirect_uri=redirect_uri or config.redirect_uri,
        scope=" ".join(scope_list),
        response_type="code",
        state=state,
        nonce=nonce,
        prompt=prompt,
        login_hint=login_hint,
        extra_params=extra_params or {},
    )

    if connection:
        auth_request.extra_params["connection"] = connection
    if audience:
        auth_request.extra_params["audience"] = audience

    params = auth_request.to_query_params()
    auth_url = f"{AUTH0_AUTHORIZE_URL}?{urlencode(params)}"

    session_data = {
        "state": state,
        "nonce": nonce,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "scopes": scope_list,
        "started_at": time.time(),
        "provider": "auth0",
        "auth_url": auth_url,
    }

    return session_data


def build_auth0_authorization_url(
    client_id: str,
    redirect_uri: str,
    scopes: Optional[list] = None,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    prompt: Optional[str] = None,
    login_hint: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
) -> Dict[str, Any]:
    state = state or generate_state()
    nonce = nonce or generate_nonce()
    scope_list = scopes or ["openid", "profile", "email"]

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scope_list),
        "response_type": "code",
        "state": state,
        "nonce": nonce,
    }

    if prompt:
        params["prompt"] = prompt
    if login_hint:
        params["login_hint"] = login_hint
    if connection:
        params["connection"] = connection
    if audience:
        params["audience"] = audience

    auth_url = f"{AUTH0_AUTHORIZE_URL}?{urlencode(params)}"

    return {
        "auth_url": auth_url,
        "state": state,
        "nonce": nonce,
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
    }


def initiate_federated_login(
    provider: str = "auth0",
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
    login_hint: Optional[str] = None,
) -> Dict[str, Any]:
    if provider == "auth0":
        config = load_oauth_config()
        return start_auth0_login(
            config=config,
            redirect_uri=redirect_uri,
            scopes=scopes,
            login_hint=login_hint,
        )
    raise ValueError(f"Unsupported provider: {provider}")
