import base64
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


@dataclass
class OAuthCallbackResult:
    access_token: str
    token_type: str
    expires_in: Optional[int]
    refresh_token: Optional[str]
    id_token: Optional[str]
    scope: Optional[str]
    raw: Dict[str, Any]


def _provider_base_url() -> str:
    return os.environ.get("OKTA_OAUTH_BASE_URL", "https://dev-00000000.okta.com/oauth2/default")


def _token_endpoint() -> str:
    return f"{_provider_base_url().rstrip('/')}/v1/token"


def _basic_auth(client_id: str, client_secret: str) -> str:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def _verify_state(expected_state: Optional[str], actual_state: Optional[str]) -> None:
    if expected_state is not None and actual_state != expected_state:
        raise ValueError("invalid_state")


def _code_verifier_from_env() -> Optional[str]:
    return os.environ.get("OAUTH_CODE_VERIFIER")


def exchange_authorization_code(
    redirect_uri: str,
    callback_url: str,
    client_id: str,
    client_secret: str,
    expected_state: Optional[str] = None,
) -> OAuthCallbackResult:
    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)
    code = (params.get("code") or [None])[0]
    state = (params.get("state") or [None])[0]
    error = (params.get("error") or [None])[0]
    error_description = (params.get("error_description") or [None])[0]

    if error:
        raise ValueError(error_description or error)
    if not code:
        raise ValueError("missing_authorization_code")
    _verify_state(expected_state, state)

    form = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    verifier = _code_verifier_from_env()
    if verifier:
        form["code_verifier"] = verifier

    data = "&".join(f"{k}={json.dumps(v)[1:-1]}" for k, v in form.items()).encode("utf-8")
    req = Request(_token_endpoint(), data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("Accept", "application/json")
    req.add_header("Authorization", _basic_auth(client_id, client_secret))

    with urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    return OAuthCallbackResult(
        access_token=payload["access_token"],
        token_type=payload.get("token_type", "Bearer"),
        expires_in=payload.get("expires_in"),
        refresh_token=payload.get("refresh_token"),
        id_token=payload.get("id_token"),
        scope=payload.get("scope"),
        raw=payload,
    )


def handle_oauth_callback(
    callback_url: str,
    redirect_uri: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    expected_state: Optional[str] = None,
) -> Dict[str, Any]:
    client_id = client_id or os.environ["OKTA_CLIENT_ID"]
    client_secret = client_secret or os.environ["OKTA_CLIENT_SECRET"]
    result = exchange_authorization_code(
        redirect_uri=redirect_uri,
        callback_url=callback_url,
        client_id=client_id,
        client_secret=client_secret,
        expected_state=expected_state,
    )
    return {
        "provider": "okta",
        "token_endpoint": _token_endpoint(),
        "tokens": {
            "access_token": result.access_token,
            "token_type": result.token_type,
            "expires_in": result.expires_in,
            "refresh_token": result.refresh_token,
            "id_token": result.id_token,
            "scope": result.scope,
        },
    }
