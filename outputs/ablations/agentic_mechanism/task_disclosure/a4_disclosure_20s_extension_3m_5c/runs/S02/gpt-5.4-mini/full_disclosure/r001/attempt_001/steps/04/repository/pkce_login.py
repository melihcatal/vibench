import base64
import hashlib
import os
import secrets
import urllib.parse
import webbrowser
from dataclasses import dataclass

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_SCOPE_ENV = "AUTH0_SCOPE"
AUTH0_CALLBACK_URL_ENV = "AUTH0_CALLBACK_URL"


@dataclass(frozen=True)
class PKCELoginResult:
    authorization_url: str
    code_verifier: str
    code_challenge: str
    state: str


def _b64url_no_padding(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def generate_code_verifier(length: int = 64) -> str:
    if length < 43 or length > 128:
        raise ValueError("PKCE code verifier length must be between 43 and 128 characters")
    return _b64url_no_padding(secrets.token_bytes(length))[:length]


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return _b64url_no_padding(digest)


def build_auth0_authorization_url(
    domain: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    code_challenge: str,
    audience: str | None = None,
) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if audience:
        params["audience"] = audience
    return f"https://{domain}/authorize?{urllib.parse.urlencode(params)}"


def start_pkce_login() -> PKCELoginResult:
    domain = os.environ[AUTH0_DOMAIN_ENV]
    client_id = os.environ[AUTH0_CLIENT_ID_ENV]
    redirect_uri = os.environ[AUTH0_CALLBACK_URL_ENV]
    scope = os.environ.get(AUTH0_SCOPE_ENV, "openid profile email")
    audience = os.environ.get(AUTH0_AUDIENCE_ENV)

    state = secrets.token_urlsafe(32)
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    authorization_url = build_auth0_authorization_url(
        domain=domain,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
        code_challenge=code_challenge,
        audience=audience,
    )
    webbrowser.open(authorization_url)
    return PKCELoginResult(
        authorization_url=authorization_url,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        state=state,
    )


def exchange_auth0_code_for_tokens(
    domain: str,
    client_id: str,
    code: str,
    redirect_uri: str,
    code_verifier: str,
) -> dict:
    token_url = f"https://{domain}/oauth/token"
    response = requests.post(
        token_url,
        json={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
