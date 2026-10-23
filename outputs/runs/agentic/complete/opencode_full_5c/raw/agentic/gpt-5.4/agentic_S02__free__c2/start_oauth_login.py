from __future__ import annotations

from identity_client import build_google_authorization_url, load_google_oidc_config
from identity_models import OAuthStartRequest


def start_oauth_login(request: OAuthStartRequest) -> dict[str, str]:
    config = load_google_oidc_config()
    redirect_uri = request.redirect_uri or config.default_redirect_uri
    authorization_url = build_google_authorization_url(
        redirect_uri=redirect_uri,
        state=request.state,
        scopes=request.scopes,
        prompt=request.prompt,
        login_hint=request.login_hint,
    )
    return {
        "provider": "google_oidc",
        "authorization_url": authorization_url,
        "redirect_uri": redirect_uri,
        "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
    }
