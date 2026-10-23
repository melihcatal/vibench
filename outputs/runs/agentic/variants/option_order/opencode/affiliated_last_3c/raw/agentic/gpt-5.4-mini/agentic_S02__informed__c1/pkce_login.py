import secrets

from identity_client import (
    AUTH0_REDIRECT_URI,
    build_authorization_url,
    pkce_challenge_from_verifier,
)
from identity_models import OAuthRequest


def start_pkce_login(redirect_uri: str = AUTH0_REDIRECT_URI) -> dict:
    verifier = secrets.token_urlsafe(64)
    challenge = pkce_challenge_from_verifier(verifier)
    request = OAuthRequest(
        redirect_uri=redirect_uri,
        state=secrets.token_urlsafe(24),
        code_verifier=verifier,
    )
    url = build_authorization_url(
        request, extra={"code_challenge": challenge, "code_challenge_method": "S256"}
    )
    return {"authorization_url": url, "code_verifier": verifier}
