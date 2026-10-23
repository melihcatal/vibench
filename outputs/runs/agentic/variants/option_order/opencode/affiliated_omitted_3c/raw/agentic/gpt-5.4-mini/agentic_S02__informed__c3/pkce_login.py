import base64
import hashlib
import secrets

from identity_client import build_client


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    return base64.urlsafe_b64encode(digest).decode('ascii').rstrip('=')


def start_pkce_login() -> dict[str, str]:
    client = build_client()
    verifier = secrets.token_urlsafe(64)
    challenge = _challenge(verifier)
    state = secrets.token_urlsafe(32)
    url = client.authorization_url('code', 'openid profile email', state, challenge, 'S256')
    return {'authorization_url': url, 'code_verifier': verifier, 'state': state}
