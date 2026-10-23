from __future__ import annotations

from identity_client import GoogleOIDCConfig, build_authorization_url
from identity_models import OAuthLoginRequest


def start_oauth_login(
    redirect_uri: str, state: str, scope: str = "openid profile email"
) -> dict:
    config = GoogleOIDCConfig.from_env(redirect_uri=redirect_uri)
    login_request = OAuthLoginRequest(
        redirect_uri=redirect_uri, state=state, scope=scope
    )
    authorization_url = build_authorization_url(config, login_request)
    return {
        "provider": "Google Identity Platform OIDC",
        "authorization_url": authorization_url,
        "state": state,
        "response_type": "code",
        "scope": scope,
    }
