import time
from typing import Any, Dict, Optional

import requests

from identity_models import (
    OAuthConfig,
    TokenResponse,
    UserProfile,
    AuditEvent,
    AuditEventType,
    parse_callback_query,
    decode_id_token_payload,
)
from identity_client import (
    load_oauth_config,
    exchange_code_for_tokens,
    fetch_user_profile,
    validate_state,
    extract_provider_from_issuer,
)


AUTH0_DOMAIN = "dev-example.auth0.com"
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}"
AUTH0_TOKEN_URL = f"{AUTH0_ISSUER}/oauth/token"


def handle_auth0_callback(
    callback_query: str,
    stored_state: str,
    config: Optional[OAuthConfig] = None,
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    params = parse_callback_query(callback_query)

    if "error" in params:
        return {
            "success": False,
            "error": params.get("error"),
            "error_description": params.get("error_description", ""),
            "provider": "auth0",
        }

    received_state = params.get("state", "")
    if not validate_state(stored_state, received_state):
        return {
            "success": False,
            "error": "invalid_state",
            "error_description": "State parameter mismatch",
            "provider": "auth0",
        }

    authorization_code = params.get("code")
    if not authorization_code:
        return {
            "success": False,
            "error": "missing_code",
            "error_description": "No authorization code in callback",
            "provider": "auth0",
        }

    if config is None:
        config = load_oauth_config()

    token_response = exchange_code_for_tokens(
        config=config,
        authorization_code=authorization_code,
        code_verifier=code_verifier,
    )

    profile = None
    if token_response.access_token:
        profile = fetch_user_profile(config, token_response.access_token)

    id_token_claims = {}
    if token_response.id_token:
        id_token_claims = decode_id_token_payload(token_response.id_token)

    audit_event = AuditEvent(
        event_id=f"evt_{int(time.time() * 1000)}",
        event_type=AuditEventType.CODE_EXCHANGED,
        timestamp=time.time(),
        user_id=profile.sub if profile else id_token_claims.get("sub"),
        provider="auth0",
        details={
            "code_exchanged": True,
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
            "has_refresh_token": token_response.refresh_token is not None,
        },
    )

    return {
        "success": True,
        "provider": "auth0",
        "token_response": token_response.to_dict(),
        "profile": profile.normalize() if profile else None,
        "id_token_claims": id_token_claims,
        "audit_event": audit_event.to_dict(),
    }


def exchange_auth0_code(
    authorization_code: str,
    redirect_uri: str,
    client_id: str,
    client_secret: str,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    if code_verifier:
        token_data["code_verifier"] = code_verifier

    response = requests.post(
        AUTH0_TOKEN_URL,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    token_json = response.json()

    return TokenResponse(
        access_token=token_json["access_token"],
        token_type=token_json.get("token_type", "Bearer"),
        expires_in=token_json.get("expires_in", 3600),
        refresh_token=token_json.get("refresh_token"),
        id_token=token_json.get("id_token"),
        scope=token_json.get("scope"),
    )


def process_callback(
    callback_url: str,
    stored_state: str,
    provider: str = "auth0",
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    if "?" in callback_url:
        query_string = callback_url.split("?", 1)[1]
    else:
        query_string = callback_url

    if provider == "auth0":
        return handle_auth0_callback(
            callback_query=query_string,
            stored_state=stored_state,
            code_verifier=code_verifier,
        )

    raise ValueError(f"Unsupported provider: {provider}")
