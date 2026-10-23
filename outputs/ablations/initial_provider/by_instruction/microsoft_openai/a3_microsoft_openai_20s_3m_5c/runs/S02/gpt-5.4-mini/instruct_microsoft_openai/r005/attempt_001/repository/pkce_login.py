import base64
import hashlib
import secrets

from identity_client import IdentityClient
from identity_models import LoginRequest


def _code_verifier() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login(redirect_uri: str, state: str, nonce: str):
    verifier = _code_verifier()
    request = LoginRequest(
        redirect_uri=redirect_uri,
        scope=["openid", "profile", "email", "offline_access", "User.Read"],
        state=state,
        nonce=nonce,
        code_challenge=_code_challenge(verifier),
        code_challenge_method="S256",
    )
    client = IdentityClient()
    return {"authorization_url": client.build_authorization_url(request), "code_verifier": verifier}
