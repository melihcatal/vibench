import hashlib
import base64
import os
import secrets
from urllib.parse import urlencode
import httpx

from identity_client import get_identity_config
from identity_models import PKCEChallenge, OAuthTokenResponse


def generate_pkce_challenge() -> PKCEChallenge:
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .replace("=", "")
    )
    return PKCEChallenge(code_verifier=code_verifier, code_challenge=code_challenge)


def start_auth0_pkce_login(
    state: str, redirect_uri: str, pkce_challenge: PKCEChallenge
):
    config = get_identity_config()
    params = {
        "client_id": config.AUTH0_CLIENT_ID,
        "response_type": "code",
        "scope": config.AUTH0_SCOPES,
        "redirect_uri": redirect_uri,
        "state": state,
        "code_challenge": pkce_challenge.code_challenge,
        "code_challenge_method": pkce_challenge.code_challenge_method,
    }
    authorization_url = f"https://{config.AUTH0_DOMAIN}/authorize?{urlencode(params)}"
    return authorization_url


async def exchange_auth0_pkce_code(
    code: str, redirect_uri: str, code_verifier: str
) -> OAuthTokenResponse:
    config = get_identity_config()
    token_url = f"https://{config.AUTH0_DOMAIN}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": config.AUTH0_CLIENT_ID,
        "code_verifier": code_verifier,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        return OAuthTokenResponse(**token_data)
