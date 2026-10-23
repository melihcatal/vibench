import base64
import hashlib
import secrets

from identity_client import build_google_authorization_url, load_identity_config
from identity_models import OAuthLoginRequest


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login() -> dict:
    config = load_identity_config()
    verifier = secrets.token_urlsafe(64)
    request = OAuthLoginRequest(redirect_uri=config["google_redirect_uri"], state=secrets.token_urlsafe(16), nonce=secrets.token_urlsafe(16))
    return {"authorization_url": build_google_authorization_url(config["google_client_id"], request, _code_challenge(verifier)), "code_verifier": verifier}
