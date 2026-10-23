import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import (
    OAuthConfig,
    TokenResponse,
    UserProfile,
    AuditEvent,
    AuditEventType,
    generate_state,
    generate_nonce,
    generate_code_verifier,
    generate_code_challenge,
)
from identity_client import (
    load_oauth_config,
    exchange_code_for_tokens,
    fetch_user_profile,
    extract_provider_from_issuer,
)


AUTH0_DOMAIN = "dev-example.auth0.com"
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}"
AUTH0_AUTHORIZE_URL = f"{AUTH0_ISSUER}/authorize"
AUTH0_TOKEN_URL = f"{AUTH0_ISSUER}/oauth/token"


def start_pkce_login(
    config: Optional[OAuthConfig] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
    code_verifier: Optional[str] = None,
    login_hint: Optional[str] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_oauth_config()

    verifier = code_verifier or generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    state = generate_state()
    nonce = generate_nonce()
    scope_list = scopes if scopes is not None else config.scopes

    params = {
        "client_id": config.client_id,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "scope": " ".join(scope_list),
        "response_type": "code",
        "state": state,
        "nonce": nonce,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    if login_hint:
        params["login_hint"] = login_hint

    auth_url = f"{AUTH0_AUTHORIZE_URL}?{urlencode(params)}"

    session_data = {
        "state": state,
        "nonce": nonce,
        "code_verifier": verifier,
        "code_challenge": challenge,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "scopes": scope_list,
        "auth_url": auth_url,
        "started_at": time.time(),
        "provider": "auth0",
        "flow_type": "pkce",
    }

    return session_data


def complete_pkce_login(
    authorization_code: str,
    code_verifier: str,
    redirect_uri: str,
    client_id: str,
    config: Optional[OAuthConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_oauth_config()

    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": code_verifier,
    }

    response = requests.post(
        AUTH0_TOKEN_URL,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    token_json = response.json()

    token_response = TokenResponse(
        access_token=token_json["access_token"],
        token_type=token_json.get("token_type", "Bearer"),
        expires_in=token_json.get("expires_in", 3600),
        refresh_token=token_json.get("refresh_token"),
        id_token=token_json.get("id_token"),
        scope=token_json.get("scope"),
    )

    profile = None
    if token_response.access_token:
        profile = fetch_user_profile(config, token_response.access_token)

    audit_event = AuditEvent(
        event_id=f"evt_{int(time.time() * 1000)}",
        event_type=AuditEventType.LOGIN_INITIATED,
        timestamp=time.time(),
        user_id=profile.sub if profile else None,
        provider="auth0",
        details={
            "flow_type": "pkce",
            "code_challenge_method": "S256",
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
        },
    )

    return {
        "success": True,
        "provider": "auth0",
        "flow_type": "pkce",
        "token_response": token_response.to_dict(),
        "profile": profile.normalize() if profile else None,
        "audit_event": audit_event.to_dict(),
    }


def generate_pkce_pair() -> Dict[str, str]:
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    return {
        "code_verifier": verifier,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }


def build_pkce_authorization_url(
    client_id: str,
    redirect_uri: str,
    code_challenge: str,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    scopes: Optional[list] = None,
    login_hint: Optional[str] = None,
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
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    if login_hint:
        params["login_hint"] = login_hint

    auth_url = f"{AUTH0_AUTHORIZE_URL}?{urlencode(params)}"

    return {
        "auth_url": auth_url,
        "state": state,
        "nonce": nonce,
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
        "flow_type": "pkce",
    }


def execute_pkce_flow(
    client_id: str,
    redirect_uri: str,
    scopes: Optional[list] = None,
    login_hint: Optional[str] = None,
) -> Dict[str, Any]:
    pkce_pair = generate_pkce_pair()
    session = start_pkce_login(
        redirect_uri=redirect_uri,
        scopes=scopes,
        code_verifier=pkce_pair["code_verifier"],
        login_hint=login_hint,
    )
    return {
        "session": session,
        "pkce_pair": pkce_pair,
        "auth_url": session["auth_url"],
    }
