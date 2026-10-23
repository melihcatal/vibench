import hashlib
import os
import base64
import secrets
from typing import Dict, Optional

from identity_models import OAuthRequest


GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"


def load_identity_config() -> Dict[str, str]:
    return {
        "google_client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
        "google_client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
        "google_redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost/callback"),
    }


def new_state() -> str:
    return secrets.token_urlsafe(24)


def new_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")


def build_google_login_request(scope: str = "openid email profile") -> OAuthRequest:
    config = load_identity_config()
    return OAuthRequest(
        client_id=config["google_client_id"],
        redirect_uri=config["google_redirect_uri"],
        scope=scope,
        state=new_state(),
    )
