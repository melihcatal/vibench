from __future__ import annotations

from typing import Iterable, Optional

from identity_client import (
    build_authorization_url,
    ensure_scopes,
    generate_nonce,
    generate_state,
)
from identity_models import OAuthLoginRequest


def start_oauth_login(
    redirect_uri: str,
    scopes: Optional[Iterable[str]] = None,
    prompt: Optional[str] = None,
    login_hint: Optional[str] = None,
) -> dict:
    state = generate_state()
    nonce = generate_nonce()
    request = OAuthLoginRequest(
        state=state,
        redirect_uri=redirect_uri,
        scopes=ensure_scopes(scopes),
        prompt=prompt,
        login_hint=login_hint,
        nonce=nonce,
    )
    authorization_url = build_authorization_url(request)
    return {
        "provider": "auth0",
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "issuer": f"https://{__import__('os').environ['AUTH0_DOMAIN']}/",
    }
