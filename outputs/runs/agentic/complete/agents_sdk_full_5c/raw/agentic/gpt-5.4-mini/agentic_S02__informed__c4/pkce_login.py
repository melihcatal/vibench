from __future__ import annotations

import secrets
from urllib.parse import urlencode

from identity_client import make_pkce_pair, load_identity_config


def build_pkce_login_url() -> tuple[str, str]:
    cfg = load_identity_config()
    verifier, challenge = make_pkce_pair()
    params = {
        "response_type": "code",
        "client_id": cfg["client_id"],
        "redirect_uri": cfg["redirect_uri"],
        "scope": "openid profile email",
        "state": secrets.token_urlsafe(16),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    base = f"https://{cfg['issuer']}/authorize" if not cfg["issuer"].startswith("https://") else f"{cfg['issuer']}/authorize"
    return f"{base}?{urlencode(params)}", verifier
