import os
import time
import secrets
import hashlib
import base64
import urllib.parse
import requests
from identity_client import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_SCOPE,
    AUTH0_AUDIENCE,
    _auth0_base_url,
)
from identity_models import TokenResponse, PKCEState, CallbackResult


def generate_code_verifier():
    return secrets.token_urlsafe(64)


def generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_pkce_authorization_url(
    code_verifier, state=None, nonce=None, extra_params=None
):
    if not state:
        state = secrets.token_urlsafe(32)
    if not nonce:
        nonce = secrets.token_urlsafe(32)
    code_challenge = generate_code_challenge(code_verifier)
    base = _auth0_base_url()
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    if extra_params:
        params.update(extra_params)
    authorize_url = f"{base}/authorize?{urllib.parse.urlencode(params)}"
    return authorize_url, state, nonce, code_challenge


def start_pkce_login(code_verifier=None, state=None, nonce=None, extra_params=None):
    if not code_verifier:
        code_verifier = generate_code_verifier()
    authorize_url, state, nonce, code_challenge = build_pkce_authorization_url(
        code_verifier, state, nonce, extra_params
    )
    return PKCEState(
        authorize_url=authorize_url,
        state=state,
        nonce=nonce,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        provider="auth0",
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=AUTH0_REDIRECT_URI,
        scope=AUTH0_SCOPE,
        timestamp=time.time(),
    )


def exchange_pkce_code(authorization_code, code_verifier):
    token_url = f"{_auth0_base_url()}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_verifier": code_verifier,
    }
    response = requests.post(token_url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data.get("access_token", ""),
        id_token=data.get("id_token", ""),
        refresh_token=data.get("refresh_token", ""),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 0),
        scope=data.get("scope", ""),
        raw=data,
    )


def complete_pkce_login(query_params, pkce_state):
    code = query_params.get("code", "")
    state = query_params.get("state", "")
    error = query_params.get("error", "")
    if error:
        error_description = query_params.get("error_description", "Unknown error")
        return CallbackResult(
            success=False,
            error=error,
            error_description=error_description,
            tokens=None,
            provider="auth0",
        )
    if state != pkce_state.state:
        return CallbackResult(
            success=False,
            error="invalid_state",
            error_description="State mismatch in PKCE flow",
            tokens=None,
            provider="auth0",
        )
    tokens = exchange_pkce_code(code, pkce_state.code_verifier)
    return CallbackResult(
        success=True,
        error=None,
        error_description=None,
        tokens=tokens,
        provider="auth0",
        timestamp=time.time(),
    )
