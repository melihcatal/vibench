import base64
import hashlib
import secrets

from identity_client import authorize_url, exchange_code
from identity_models import IdentityRequest, TokenResponse


def pkce_verifier() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode()


def pkce_challenge(verifier: str) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()


def pkce_login(redirect_uri: str, state: str, nonce: str = '') -> tuple[str, str]:
    verifier = pkce_verifier()
    request = IdentityRequest(redirect_uri=redirect_uri, state=state, nonce=nonce or None, code_verifier=verifier)
    return authorize_url(request), verifier


def finish_pkce_login(code: str, redirect_uri: str, code_verifier: str) -> TokenResponse:
    return exchange_code(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier)
