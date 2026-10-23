import base64
import hashlib
import secrets

from identity_client import build_authorization_url
from identity_models import OAuthLoginRequest


def create_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def create_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")


def start_pkce_login(redirect_uri: str, state: str = None):
    verifier = create_code_verifier()
    challenge = create_code_challenge(verifier)
    request = OAuthLoginRequest(redirect_uri=redirect_uri, state=state)
    return {"authorization_url": build_authorization_url(request, code_challenge=challenge), "code_verifier": verifier}
