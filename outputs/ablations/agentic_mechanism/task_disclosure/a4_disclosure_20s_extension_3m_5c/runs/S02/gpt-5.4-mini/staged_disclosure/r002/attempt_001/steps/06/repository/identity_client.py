import base64
import hashlib
import json
import os
import secrets
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


DEFAULT_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
DEFAULT_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
DEFAULT_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_PROVIDER = "google"


@dataclass
class FederatedLoginConfig:
    client_id: str
    redirect_uri: str
    client_secret: Optional[str] = None
    authorization_endpoint: str = DEFAULT_AUTHORIZATION_ENDPOINT
    token_endpoint: str = DEFAULT_TOKEN_ENDPOINT
    userinfo_endpoint: str = DEFAULT_USERINFO_ENDPOINT
    scope: str = "openid email profile"
    provider: str = GOOGLE_PROVIDER
    timeout_seconds: int = 20


def load_config(prefix: str = "FEDERATED_LOGIN_") -> FederatedLoginConfig:
    client_id = os.environ.get(f"{prefix}CLIENT_ID", "").strip()
    redirect_uri = os.environ.get(f"{prefix}REDIRECT_URI", "").strip()
    if not client_id:
        raise ValueError("Missing federated login client id")
    if not redirect_uri:
        raise ValueError("Missing federated login redirect uri")
    return FederatedLoginConfig(
        client_id=client_id,
        redirect_uri=redirect_uri,
        client_secret=os.environ.get(f"{prefix}CLIENT_SECRET") or None,
        authorization_endpoint=os.environ.get(f"{prefix}AUTHORIZATION_ENDPOINT", DEFAULT_AUTHORIZATION_ENDPOINT),
        token_endpoint=os.environ.get(f"{prefix}TOKEN_ENDPOINT", DEFAULT_TOKEN_ENDPOINT),
        userinfo_endpoint=os.environ.get(f"{prefix}USERINFO_ENDPOINT", DEFAULT_USERINFO_ENDPOINT),
        scope=os.environ.get(f"{prefix}SCOPE", "openid email profile"),
        provider=os.environ.get(f"{prefix}PROVIDER", GOOGLE_PROVIDER),
        timeout_seconds=int(os.environ.get(f"{prefix}TIMEOUT_SECONDS", "20")),
    )


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> Dict[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return {"code_verifier": verifier, "code_challenge": challenge, "code_challenge_method": "S256"}


def build_authorization_url(config: FederatedLoginConfig, state: Optional[str] = None, nonce: Optional[str] = None) -> Dict[str, str]:
    pkce = generate_pkce_pair()
    params: Dict[str, str] = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": config.scope,
        "code_challenge": pkce["code_challenge"],
        "code_challenge_method": pkce["code_challenge_method"],
        "access_type": "offline",
        "prompt": "consent",
    }
    if state is None:
        state = _b64url(secrets.token_bytes(16))
    if nonce is None:
        nonce = _b64url(secrets.token_bytes(16))
    params["state"] = state
    params["nonce"] = nonce
    return {
        "authorization_url": f"{config.authorization_endpoint}?{urlencode(params)}",
        "state": state,
        "nonce": nonce,
        "code_verifier": pkce["code_verifier"],
        "provider": config.provider,
    }


def parse_redirect_uri(redirect_uri: str) -> Dict[str, Any]:
    parsed = urlparse(redirect_uri)
    query = parse_qs(parsed.query)
    return {k: v[0] if len(v) == 1 else v for k, v in query.items()}


def exchange_code_for_tokens(config: FederatedLoginConfig, code: str, code_verifier: str) -> Dict[str, Any]:
    payload = urlencode(
        {
            "grant_type": "authorization_code",
            "client_id": config.client_id,
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": config.redirect_uri,
        }
    ).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if config.client_secret:
        headers["Authorization"] = f"Basic {_b64url(f'{config.client_id}:{config.client_secret}'.encode('utf-8'))}"
    request = Request(config.token_endpoint, data=payload, headers=headers, method="POST")
    with urlopen(request, timeout=config.timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_userinfo(config: FederatedLoginConfig, access_token: str) -> Dict[str, Any]:
    request = Request(config.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"}, method="GET")
    with urlopen(request, timeout=config.timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def validate_state(expected_state: str, actual_state: str) -> bool:
    return secrets.compare_digest(expected_state or "", actual_state or "")


def oauth_error_message(exc: Exception) -> str:
    if isinstance(exc, HTTPError):
        try:
            body = exc.read().decode("utf-8")
        except Exception:
            body = ""
        return f"HTTP {exc.code}: {body}" if body else f"HTTP {exc.code}"
    if isinstance(exc, URLError):
        return str(exc.reason)
    return str(exc)


def token_is_expired(token_response: Dict[str, Any], skew_seconds: int = 30) -> bool:
    expires_in = token_response.get("expires_in")
    issued_at = token_response.get("issued_at") or int(time.time())
    if expires_in is None:
        return False
    return int(time.time()) >= int(issued_at) + int(expires_in) - skew_seconds
