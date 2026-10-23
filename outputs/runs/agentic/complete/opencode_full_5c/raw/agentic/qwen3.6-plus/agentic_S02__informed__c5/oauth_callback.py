import os
import time
import requests
from identity_client import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_REDIRECT_URI,
    _auth0_base_url,
)
from identity_models import TokenResponse, CallbackResult


def exchange_code_for_tokens(authorization_code, code_verifier=None):
    token_url = f"{_auth0_base_url()}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
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


def verify_state(received_state, expected_state):
    return received_state == expected_state


def handle_oauth_callback(query_params, expected_state=None, code_verifier=None):
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
    if expected_state and not verify_state(state, expected_state):
        return CallbackResult(
            success=False,
            error="invalid_state",
            error_description="State mismatch detected",
            tokens=None,
            provider="auth0",
        )
    tokens = exchange_code_for_tokens(code, code_verifier)
    return CallbackResult(
        success=True,
        error=None,
        error_description=None,
        tokens=tokens,
        provider="auth0",
        timestamp=time.time(),
    )
