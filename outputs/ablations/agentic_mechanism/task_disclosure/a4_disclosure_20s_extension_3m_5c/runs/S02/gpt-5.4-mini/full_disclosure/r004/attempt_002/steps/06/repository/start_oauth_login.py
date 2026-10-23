import base64
import hashlib
import os
import secrets
import urllib.parse


AUTH0_AUTHORIZE_URL = "https://{domain}/authorize"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def build_authorization_url(
    domain: str,
    client_id: str,
    redirect_uri: str,
    scope: str = "openid profile email",
    audience: str | None = None,
    state: str | None = None,
    code_verifier: str | None = None,
) -> tuple[str, str, str]:
    if not domain:
        raise ValueError("domain is required")
    if not client_id:
        raise ValueError("client_id is required")
    if not redirect_uri:
        raise ValueError("redirect_uri is required")

    state_value = state or secrets.token_urlsafe(32)
    verifier = code_verifier or secrets.token_urlsafe(64)
    challenge = _b64url(hashlib.sha256(verifier.encode("utf-8")).digest())

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state_value,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if audience:
        params["audience"] = audience

    url = AUTH0_AUTHORIZE_URL.format(domain=domain) + "?" + urllib.parse.urlencode(params)
    return url, state_value, verifier


def start_oauth_login() -> dict[str, str]:
    domain = os.environ.get("AUTH0_DOMAIN", "")
    client_id = os.environ.get("AUTH0_CLIENT_ID", "")
    redirect_uri = os.environ.get("AUTH0_REDIRECT_URI", "")
    scope = os.environ.get("AUTH0_SCOPE", "openid profile email")
    audience = os.environ.get("AUTH0_AUDIENCE")
    authorization_url, state, code_verifier = build_authorization_url(
        domain=domain,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
    )
    return {
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": code_verifier,
        "provider": "auth0",
    }
