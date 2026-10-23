import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

from identity_models import OAuthClientConfig, AuthorizationResult


GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_ISSUER = "https://accounts.google.com"


def load_google_config() -> OAuthClientConfig:
    return OAuthClientConfig(
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
        authorization_endpoint=GOOGLE_AUTHORIZATION_ENDPOINT,
        token_endpoint=GOOGLE_TOKEN_ENDPOINT,
        userinfo_endpoint=GOOGLE_USERINFO_ENDPOINT,
        issuer=GOOGLE_ISSUER,
    )


def new_state() -> str:
    return secrets.token_urlsafe(32)


def new_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def code_challenge_s256(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_google_authorization_url(config: OAuthClientConfig, state: str, code_challenge: Optional[str] = None) -> str:
    from urllib.parse import urlencode

    params: Dict[str, str] = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": config.scope,
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return f"{config.authorization_endpoint}?{urlencode(params)}"


def build_authorization_result(config: OAuthClientConfig, use_pkce: bool = False) -> AuthorizationResult:
    state = new_state()
    verifier = new_code_verifier() if use_pkce else None
    challenge = code_challenge_s256(verifier) if verifier else None
    return AuthorizationResult(
        authorization_url=build_google_authorization_url(config, state, challenge),
        state=state,
        code_verifier=verifier,
        code_challenge=challenge,
    )
