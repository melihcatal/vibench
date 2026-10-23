import base64
import hashlib
import secrets
import urllib.parse

from identity_client import load_identity_config


def create_pkce_pair():
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return verifier, challenge


def build_pkce_login_url() -> str:
    cfg = load_identity_config()
    verifier, challenge = create_pkce_pair()
    params = {
        "response_type": "code",
        "client_id": cfg["cognito_user_pool_client_id"],
        "redirect_uri": cfg["redirect_uri"],
        "scope": cfg["scope"],
        "state": secrets.token_urlsafe(24),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return verifier + "|" + f"https://{cfg['cognito_domain']}/oauth2/authorize?{urllib.parse.urlencode(params)}"
