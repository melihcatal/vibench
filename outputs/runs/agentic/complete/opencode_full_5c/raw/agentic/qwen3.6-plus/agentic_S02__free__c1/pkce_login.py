import os
from typing import Optional, Dict, Any

from identity_models import OAuthConfig, TokenResponse, normalize_azure_claims
from identity_client import (
    build_authorization_url,
    exchange_authorization_code,
    fetch_userinfo,
    generate_pkce_pair,
)


AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID", "common")
AZURE_AUTHORIZE_URL = (
    f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/authorize"
)
AZURE_TOKEN_URL = (
    f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token"
)
AZURE_USERINFO_URL = "https://graph.microsoft.com/oidc/userinfo"
AZURE_GRAPH_URL = "https://graph.microsoft.com/v1.0/me"


def build_azure_config(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
    tenant_id: Optional[str] = None,
) -> OAuthConfig:
    tid = tenant_id or AZURE_TENANT_ID
    return OAuthConfig(
        provider="azure_ad",
        client_id=client_id or os.environ.get("AZURE_CLIENT_ID", ""),
        redirect_uri=redirect_uri
        or os.environ.get("AZURE_REDIRECT_URI", "http://localhost:3000/callback"),
        authorize_url=f"https://login.microsoftonline.com/{tid}/oauth2/v2.0/authorize",
        token_url=f"https://login.microsoftonline.com/{tid}/oauth2/v2.0/token",
        userinfo_url=AZURE_USERINFO_URL,
        scopes=scopes or ["openid", "profile", "email", "User.Read"],
    )


def start_pkce_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
    tenant_id: Optional[str] = None,
    state: Optional[str] = None,
    prompt: Optional[str] = None,
    domain_hint: Optional[str] = None,
) -> Dict[str, Any]:
    import secrets
    from identity_models import generate_state as gen_state

    config = build_azure_config(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=scopes,
        tenant_id=tenant_id,
    )

    code_verifier, code_challenge = generate_pkce_pair()
    auth_state = state or gen_state()

    extra = {}
    if prompt:
        extra["prompt"] = prompt
    if domain_hint:
        extra["domain_hint"] = domain_hint
    config.extra_params = extra

    authorization_url = build_authorization_url(
        config=config,
        state=auth_state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    return {
        "authorization_url": authorization_url,
        "state": auth_state,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "provider": "azure_ad",
        "tenant_id": tid if (tid := tenant_id or AZURE_TENANT_ID) else None,
        "authorize_endpoint": AZURE_AUTHORIZE_URL,
    }


def complete_pkce_login(
    authorization_code: str,
    code_verifier: str,
    expected_state: Optional[str] = None,
    received_state: Optional[str] = None,
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> Dict[str, Any]:
    if expected_state and received_state and expected_state != received_state:
        raise ValueError("State mismatch: possible CSRF attack")

    config = build_azure_config(
        client_id=client_id,
        redirect_uri=redirect_uri,
        tenant_id=tenant_id,
    )

    token_response: TokenResponse = exchange_authorization_code(
        config=config,
        code=authorization_code,
        code_verifier=code_verifier,
    )

    profile = None
    if token_response.access_token:
        import requests

        headers = {"Authorization": f"Bearer {token_response.access_token}"}
        resp = requests.get(AZURE_GRAPH_URL, headers=headers, timeout=30)
        if resp.status_code == 200:
            graph_data = resp.json()
            profile = normalize_azure_claims(graph_data)

    return {
        "token_response": token_response.to_dict(),
        "profile": profile.to_dict() if profile else None,
        "provider": "azure_ad",
        "tenant_id": tenant_id or AZURE_TENANT_ID,
        "token_endpoint": AZURE_TOKEN_URL,
    }


def refresh_azure_token(
    refresh_token: str,
    client_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
) -> TokenResponse:
    import requests

    tid = tenant_id or AZURE_TENANT_ID
    token_url = f"https://login.microsoftonline.com/{tid}/oauth2/v2.0/token"

    body = {
        "grant_type": "refresh_token",
        "client_id": client_id or os.environ.get("AZURE_CLIENT_ID", ""),
        "refresh_token": refresh_token,
    }

    resp = requests.post(token_url, data=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    return TokenResponse(
        access_token=data["access_token"],
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 3600),
        refresh_token=data.get("refresh_token"),
        scope=data.get("scope"),
        raw_response=data,
    )
