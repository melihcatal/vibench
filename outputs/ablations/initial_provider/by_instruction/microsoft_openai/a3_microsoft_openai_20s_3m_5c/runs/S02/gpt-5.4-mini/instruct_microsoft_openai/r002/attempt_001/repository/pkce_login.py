import base64
import hashlib
import secrets

from start_oauth_login import build_login_url


def generate_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
    return verifier, challenge


def build_pkce_login_url() -> tuple[str, str]:
    verifier, challenge = generate_pkce_pair()
    return build_login_url(code_challenge=challenge), verifier
