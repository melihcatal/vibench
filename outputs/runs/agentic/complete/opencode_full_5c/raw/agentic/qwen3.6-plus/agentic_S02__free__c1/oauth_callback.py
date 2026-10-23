import os
from typing import Optional, Dict, Any

from identity_models import OAuthConfig, TokenResponse, normalize_auth0_claims
from identity_client import (
    exchange_authorization_code,
    fetch_userinfo,
    validate_id_token,
)


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-123456.us.auth0.com")
AUTH0_AUTHORIZE_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"


def build_auth0_config(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
) -> OAuthConfig:
    return OAuthConfig(
        provider="auth0",
        client_id=client_id or os.environ.get("AUTH0_CLIENT_ID", ""),
        client_secret=client_secret or os.environ.get("AUTH0_CLIENT_SECRET"),
        redirect_uri=redirect_uri
        or os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:3000/callback"),
        authorize_url=AUTH0_AUTHORIZE_URL,
        token_url=AUTH0_TOKEN_URL,
        userinfo_url=AUTH0_USERINFO_URL,
        scopes=scopes or ["openid", "profile", "email"],
    )


def handle_auth0_callback(
    authorization_code: str,
    expected_state: Optional[str] = None,
    received_state: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    if expected_state and received_state and expected_state != received_state:
        raise ValueError("State mismatch: possible CSRF attack")

    config = build_auth0_config(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    token_response = exchange_authorization_code(
        config=config,
        code=authorization_code,
        code_verifier=code_verifier,
    )

    profile = None
    id_token_payload = None
    if token_response.id_token:
        id_token_payload = validate_id_token(token_response.id_token)

    if token_response.access_token:
        userinfo = fetch_userinfo(config, token_response.access_token)
        profile = normalize_auth0_claims(userinfo)

    return {
        "token_response": token_response.to_dict(),
        "profile": profile.to_dict() if profile else None,
        "id_token_payload": id_token_payload,
        "provider": "auth0",
        "auth0_domain": AUTH0_DOMAIN,
    }


def handle_auth0_callback_with_pkce(
    authorization_code: str,
    code_verifier: str,
    expected_state: Optional[str] = None,
    received_state: Optional[str] = None,
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> Dict[str, Any]:
    return handle_auth0_callback(
        authorization_code=authorization_code,
        expected_state=expected_state,
        received_state=received_state,
        client_id=client_id,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
