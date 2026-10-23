from __future__ import annotations

from typing import Dict, Optional

from identity_client import build_authorization_url, load_auth0_settings
from identity_models import OAuthStartRequest


PROVIDER = "Auth0 Authentication API"



def start_oauth_login(
    redirect_uri: str,
    state: str,
    scopes: Optional[list[str]] = None,
    prompt: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
) -> Dict[str, str]:
    settings = load_auth0_settings()
    request = OAuthStartRequest(
        redirect_uri=redirect_uri,
        state=state,
        scopes=scopes or ["openid", "profile", "email"],
        prompt=prompt,
        connection=connection,
        audience=audience,
    )
    authorization_url = build_authorization_url(
        settings=settings,
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=" ".join(request.scopes),
        prompt=request.prompt,
        audience=request.audience,
        connection=request.connection,
    )
    return {
        "provider": PROVIDER,
        "authorization_url": authorization_url,
        "issuer": settings.issuer,
        "client_id": settings.client_id,
    }
