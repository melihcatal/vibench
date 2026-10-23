import base64
import hashlib
import secrets
from urllib.parse import urlencode

from identity_client import build_oidc_config, build_state_payload, redirect_uri_for


def _code_verifier() -> str:
    return secrets.token_urlsafe(64)


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def start_pkce_login(redirect_uri: str | None = None) -> dict:
    cfg = build_oidc_config()
    verifier = _code_verifier()
    challenge = _code_challenge(verifier)
    redirect = redirect_uri or redirect_uri_for(cfg)
    state = build_state_payload({"flow": "pkce", "verifier_hint": verifier[:8]})
    params = {
        "client_id": cfg.client_id,
        "response_type": "code",
        "response_mode": "query",
        "redirect_uri": redirect,
        "scope": cfg.scopes,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return {"authorization_url": f"{cfg.authorization_endpoint()}?{urlencode(params)}", "code_verifier": verifier, "state": state}
