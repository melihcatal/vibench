import os
import secrets
from typing import Dict, List

from authlib.integrations.requests_client import OAuth2Session


def auth0_domain() -> str:
    return os.environ["AUTH0_DOMAIN"]


def auth0_client_id() -> str:
    return os.environ["AUTH0_CLIENT_ID"]


def auth0_client_secret() -> str:
    return os.environ.get("AUTH0_CLIENT_SECRET", "")


def issuer_base_url() -> str:
    return f"https://{auth0_domain()}"


def authorize_url() -> str:
    return f"{issuer_base_url()}/authorize"


def token_url() -> str:
    return f"{issuer_base_url()}/oauth/token"


def userinfo_url() -> str:
    return f"{issuer_base_url()}/userinfo"


def oidc_session(redirect_uri: str, scope: List[str]) -> OAuth2Session:
    return OAuth2Session(
        client_id=auth0_client_id(),
        client_secret=auth0_client_secret(),
        scope=scope,
        redirect_uri=redirect_uri,
    )


def random_state() -> str:
    return secrets.token_urlsafe(32)


def random_nonce() -> str:
    return secrets.token_urlsafe(32)


def pkce_verifier() -> str:
    return secrets.token_urlsafe(64)


def pkce_challenge(verifier: str) -> str:
    import base64
    import hashlib

    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
