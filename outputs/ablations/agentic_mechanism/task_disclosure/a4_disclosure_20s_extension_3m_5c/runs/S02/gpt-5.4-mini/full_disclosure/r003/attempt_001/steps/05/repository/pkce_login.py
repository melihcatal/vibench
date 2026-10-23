import base64
import hashlib
import json
import os
import secrets
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Dict, Optional

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"

@dataclass(frozen=True)
class PKCELoginConfig:
    client_id: str
    redirect_uri: str
    scope: str = "openid email profile"
    auth_endpoint: str = GOOGLE_AUTH_ENDPOINT
    token_endpoint: str = GOOGLE_TOKEN_ENDPOINT
    userinfo_endpoint: str = GOOGLE_USERINFO_ENDPOINT


def _base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_code_verifier(length: int = 64) -> str:
    if not 43 <= length <= 128:
        raise ValueError("PKCE verifier length must be between 43 and 128")
    return _base64url(secrets.token_bytes(length))[:length]


def generate_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return _base64url(digest)


def build_authorization_url(config: PKCELoginConfig, state: Optional[str] = None, code_verifier: Optional[str] = None) -> Dict[str, str]:
    verifier = code_verifier or generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": config.scope,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if state is None:
        state = _base64url(secrets.token_bytes(16))
    params["state"] = state
    return {"authorization_url": f"{config.auth_endpoint}?{urllib.parse.urlencode(params)}", "state": state, "code_verifier": verifier}


def exchange_code_for_tokens(config: PKCELoginConfig, code: str, code_verifier: str) -> Dict[str, object]:
    payload = urllib.parse.urlencode({
        "client_id": config.client_id,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.redirect_uri,
        "code_verifier": code_verifier,
    }).encode("utf-8")
    request = urllib.request.Request(config.token_endpoint, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_userinfo(config: PKCELoginConfig, access_token: str) -> Dict[str, object]:
    request = urllib.request.Request(config.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def pkce_login_flow(client_id: Optional[str] = None, redirect_uri: Optional[str] = None, code: Optional[str] = None, state: Optional[str] = None, code_verifier: Optional[str] = None) -> Dict[str, object]:
    client_id = client_id or os.environ["GOOGLE_OAUTH_CLIENT_ID"]
    redirect_uri = redirect_uri or os.environ["GOOGLE_OAUTH_REDIRECT_URI"]
    config = PKCELoginConfig(client_id=client_id, redirect_uri=redirect_uri)
    if code is None:
        return build_authorization_url(config, state=state, code_verifier=code_verifier)
    if code_verifier is None:
        raise ValueError("code_verifier is required to exchange the authorization code")
    tokens = exchange_code_for_tokens(config, code, code_verifier)
    result = {"tokens": tokens}
    access_token = tokens.get("access_token")
    if isinstance(access_token, str) and access_token:
        result["userinfo"] = fetch_userinfo(config, access_token)
    return result
