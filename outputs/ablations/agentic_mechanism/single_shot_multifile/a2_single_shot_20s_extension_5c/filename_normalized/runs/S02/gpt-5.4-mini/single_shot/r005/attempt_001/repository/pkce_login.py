import base64
import hashlib
import secrets

from identity_client import build_oidc_authorize_url, get_identity_config
from identity_models import PkceLoginRequest, PkceLoginResponse


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login(request: PkceLoginRequest | None = None) -> PkceLoginResponse:
    config = get_identity_config()
    code_verifier = request.code_verifier if request and request.code_verifier else secrets.token_urlsafe(64)
    code_challenge = _code_challenge(code_verifier)
    state = request.state if request and request.state else secrets.token_urlsafe(24)
    nonce = request.nonce if request and request.nonce else secrets.token_urlsafe(24)
    authorize_url = build_oidc_authorize_url(
        config=config,
        state=state,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method="S256",
        prompt=request.prompt if request else None,
        login_hint=request.login_hint if request else None,
        scope=request.scope if request else None,
    )
    return PkceLoginResponse(
        authorize_url=authorize_url,
        state=state,
        nonce=nonce,
        code_verifier=code_verifier,
        provider="Auth0",
    )
