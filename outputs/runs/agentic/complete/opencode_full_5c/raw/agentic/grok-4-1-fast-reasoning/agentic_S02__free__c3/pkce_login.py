import secrets
import hashlib
import base64
import webbrowser
from urllib.parse import urlencode
from .identity_client import get_google_pkce_config
from .identity_models import OAuthConfig
from typing import Tuple


def generate_pkce_pair() -> Tuple[str, str]:
    verifier = (
        base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
    )
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )
    return verifier, challenge


def generate_pkce_auth_url(config: OAuthConfig) -> Tuple[str, str]:
    verifier, challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": " ".join(config.scopes),
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    url = config.auth_url + "?" + urlencode(params)
    return url, verifier


def start_pkce_login():
    config = get_google_pkce_config()
    url, verifier = generate_pkce_auth_url(config)
    print(f"PKCE Verifier (save for callback): {verifier}")
    print(f"Opening Google PKCE URL: {url}")
    webbrowser.open(url)
