import base64
import hashlib
import secrets
from urllib.parse import urlencode
from identity_client import get_oidc_config, build_redirect_uri


def _challenge(verifier):
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def create_pkce_login(scope=None):
    cfg = get_oidc_config()
    verifier = secrets.token_urlsafe(64)
    challenge = _challenge(verifier)
    params = {
        "client_id": cfg["client_id"],
        "response_type": "code",
        "redirect_uri": build_redirect_uri(cfg),
        "scope": scope or cfg["scope"],
        "state": secrets.token_urlsafe(24),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return {"authorization_url": f"{cfg['authorization_endpoint']}?{urlencode(params)}", "code_verifier": verifier, "code_challenge": challenge}
