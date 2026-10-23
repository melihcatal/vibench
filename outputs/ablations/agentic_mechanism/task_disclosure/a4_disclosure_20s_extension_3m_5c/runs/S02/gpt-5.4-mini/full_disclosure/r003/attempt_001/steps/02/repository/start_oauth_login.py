import base64
import hashlib
import secrets
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Optional


AUTH0_AUTHORIZE_ENDPOINT = "https://YOUR_AUTH0_DOMAIN/authorize"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_SCOPE = "openid profile email"


@dataclass(frozen=True)
class OAuthLoginRequest:
    client_id: str
    redirect_uri: str
    scope: str = AUTH0_SCOPE
    audience: Optional[str] = None
    organization: Optional[str] = None
    connection: Optional[str] = None
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: str = "S256"


@dataclass(frozen=True)
class OAuthLoginResponse:
    authorization_url: str
    state: str
    nonce: str
    code_verifier: str
    code_challenge: str


def _base64url_no_padding(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def generate_pkce_pair() -> Dict[str, str]:
    code_verifier = _base64url_no_padding(secrets.token_bytes(32))
    code_challenge = _base64url_no_padding(hashlib.sha256(code_verifier.encode("ascii")).digest())
    return {"code_verifier": code_verifier, "code_challenge": code_challenge}


def build_authorization_url(request: OAuthLoginRequest) -> OAuthLoginResponse:
    state = request.state or _base64url_no_padding(secrets.token_bytes(16))
    nonce = request.nonce or _base64url_no_padding(secrets.token_bytes(16))
    pkce = generate_pkce_pair()
    code_challenge = request.code_challenge or pkce["code_challenge"]
    code_verifier = pkce["code_verifier"]

    params = {
        "client_id": request.client_id,
        "redirect_uri": request.redirect_uri,
        "response_type": "code",
        "scope": request.scope,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": request.code_challenge_method,
    }
    if request.audience:
        params["audience"] = request.audience
    if request.organization:
        params["organization"] = request.organization
    if request.connection:
        params["connection"] = request.connection

    authorization_url = AUTH0_AUTHORIZE_ENDPOINT + "?" + urllib.parse.urlencode(params)
    return OAuthLoginResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
    )


def start_oauth_login(client_id: str, redirect_uri: str, **kwargs) -> OAuthLoginResponse:
    request = OAuthLoginRequest(client_id=client_id, redirect_uri=redirect_uri, **kwargs)
    return build_authorization_url(request)
