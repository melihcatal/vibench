from __future__ import annotations

from identity_client import (
    GoogleOIDCConfig,
    build_pkce_authorization_url,
    generate_code_verifier,
)
from identity_models import PKCELoginRequest


def start_pkce_login(
    redirect_uri: str, state: str, scope: str = "openid profile email"
) -> dict:
    config = GoogleOIDCConfig.from_env(redirect_uri=redirect_uri)
    code_verifier = generate_code_verifier()
    login_request = PKCELoginRequest(
        redirect_uri=redirect_uri,
        state=state,
        code_verifier=code_verifier,
        scope=scope,
    )
    authorization_url = build_pkce_authorization_url(config, login_request)
    return {
        "provider": "Google Identity Platform OIDC",
        "authorization_url": authorization_url,
        "code_verifier": code_verifier,
        "code_challenge_method": "S256",
        "state": state,
    }
