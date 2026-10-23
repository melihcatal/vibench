import base64
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


@dataclass
class OAuthCallbackResult:
    access_token: str
    token_type: str
    expires_in: Optional[int]
    refresh_token: Optional[str]
    id_token: Optional[str]
    scope: Optional[str]
    raw: Dict[str, Any]


class OAuthCallbackError(Exception):
    pass


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sha256_b64url(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def exchange_authorization_code(
    code: str,
    redirect_uri: str,
    *,
    code_verifier: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    timeout: float = 10.0,
) -> OAuthCallbackResult:
    if not code:
        raise OAuthCallbackError("authorization code is required")
    if not redirect_uri:
        raise OAuthCallbackError("redirect_uri is required")

    client_id = client_id or os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = client_secret or os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    if not client_id:
        raise OAuthCallbackError("GOOGLE_OAUTH_CLIENT_ID is required")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
    }
    if client_secret:
        data["client_secret"] = client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier

    response = requests.post(
        GOOGLE_TOKEN_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=timeout,
    )
    if response.status_code != 200:
        raise OAuthCallbackError(f"token exchange failed: {response.status_code} {response.text}")

    payload = response.json()
    access_token = payload.get("access_token")
    token_type = payload.get("token_type")
    if not access_token or not token_type:
        raise OAuthCallbackError("token response missing required fields")

    return OAuthCallbackResult(
        access_token=access_token,
        token_type=token_type,
        expires_in=payload.get("expires_in"),
        refresh_token=payload.get("refresh_token"),
        id_token=payload.get("id_token"),
        scope=payload.get("scope"),
        raw=payload,
    )


def handle_callback(query_params: Dict[str, str], redirect_uri: str) -> Dict[str, Any]:
    error = query_params.get("error")
    if error:
        raise OAuthCallbackError(query_params.get("error_description") or error)

    code = query_params.get("code", "")
    state = query_params.get("state")
    code_verifier = query_params.get("code_verifier")
    result = exchange_authorization_code(code, redirect_uri, code_verifier=code_verifier)
    return {
        "provider": "google",
        "state": state,
        "token": {
            "access_token": result.access_token,
            "token_type": result.token_type,
            "expires_in": result.expires_in,
            "refresh_token": result.refresh_token,
            "id_token": result.id_token,
            "scope": result.scope,
        },
    }
