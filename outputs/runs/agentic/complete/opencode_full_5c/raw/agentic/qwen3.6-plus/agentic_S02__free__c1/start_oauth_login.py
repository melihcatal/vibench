import os
from typing import Optional, Dict, Any

from identity_models import OAuthConfig, generate_state, generate_nonce
from identity_client import build_authorization_url


OKTA_DOMAIN = os.environ.get("OKTA_DOMAIN", "https://dev-123456.okta.com")
OKTA_AUTHORIZE_URL = f"{OKTA_DOMAIN}/oauth2/default/v1/authorize"
OKTA_TOKEN_URL = f"{OKTA_DOMAIN}/oauth2/default/v1/token"
OKTA_USERINFO_URL = f"{OKTA_DOMAIN}/oauth2/default/v1/userinfo"


def build_okta_config(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
) -> OAuthConfig:
    return OAuthConfig(
        provider="okta",
        client_id=client_id or os.environ.get("OKTA_CLIENT_ID", ""),
        client_secret=client_secret or os.environ.get("OKTA_CLIENT_SECRET"),
        redirect_uri=redirect_uri
        or os.environ.get("OKTA_REDIRECT_URI", "http://localhost:3000/callback"),
        authorize_url=OKTA_AUTHORIZE_URL,
        token_url=OKTA_TOKEN_URL,
        userinfo_url=OKTA_USERINFO_URL,
        scopes=scopes or ["openid", "profile", "email"],
    )


def start_okta_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    prompt: Optional[str] = None,
    idp: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    config = build_okta_config(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=scopes,
    )

    auth_state = state or generate_state()
    auth_nonce = nonce or generate_nonce()

    params = {}
    if prompt:
        params["prompt"] = prompt
    if idp:
        params["idp"] = idp
    if extra_params:
        params.update(extra_params)
    config.extra_params = params

    authorization_url = build_authorization_url(
        config=config,
        state=auth_state,
        nonce=auth_nonce,
    )

    return {
        "authorization_url": authorization_url,
        "state": auth_state,
        "nonce": auth_nonce,
        "provider": "okta",
        "okta_domain": OKTA_DOMAIN,
    }


def start_okta_login_with_session(
    session: Any,
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
) -> Dict[str, Any]:
    result = start_okta_login(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=scopes,
    )
    session["okta_oauth_state"] = result["state"]
    session["okta_oauth_nonce"] = result["nonce"]
    return result
