import base64
import hashlib
import os
from typing import Dict

from identity_models import OAuthRequest


def microsoft_tenant() -> str:
    return os.environ.get("MICROSOFT_TENANT_ID", "common")


def microsoft_client_id() -> str:
    return os.environ.get("MICROSOFT_CLIENT_ID", "")


def microsoft_client_secret() -> str:
    return os.environ.get("MICROSOFT_CLIENT_SECRET", "")


def microsoft_authorize_url() -> str:
    tenant = microsoft_tenant()
    return f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"


def microsoft_token_url() -> str:
    tenant = microsoft_tenant()
    return f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"


def microsoft_userinfo_url() -> str:
    return "https://graph.microsoft.com/oidc/userinfo"


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def oauth_request(redirect_uri: str, state: str, code_verifier: str) -> OAuthRequest:
    return OAuthRequest(
        redirect_uri=redirect_uri,
        state=state,
        code_verifier=code_verifier,
        code_challenge=pkce_challenge(code_verifier),
    )


def token_payload(code: str, redirect_uri: str, code_verifier: str) -> Dict[str, str]:
    return {
        "client_id": microsoft_client_id(),
        "client_secret": microsoft_client_secret(),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
        "scope": "openid profile email offline_access",
    }
