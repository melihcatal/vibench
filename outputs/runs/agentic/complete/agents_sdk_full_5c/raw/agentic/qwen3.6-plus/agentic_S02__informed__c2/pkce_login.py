"""
pkce_login.py - Implements a PKCE (Proof Key for Code Exchange) login flow
for public clients.

Provider: Amazon Cognito Hosted UI Federation
SDK: boto3 (cognito-idp) + requests for OIDC endpoints
Auth env vars: COGNITO_DOMAIN, COGNITO_CLIENT_ID
"""

import base64
import hashlib
import os
import secrets
import urllib.parse
from typing import Optional

import boto3
import requests


def generate_pkce_pair() -> tuple[str, str]:
    """
    Generate a PKCE code verifier and code challenge (S256 method).
    """
    code_verifier = secrets.token_urlsafe(64)
    code_verifier_bytes = code_verifier.encode("ascii")
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier_bytes).digest()
    ).rstrip(b"=").decode("ascii")
    return code_verifier, code_challenge


def build_pkce_auth_url(
    redirect_uri: str,
    scope: str = "openid profile email",
    state: Optional[str] = None,
) -> dict:
    """
    Build the Amazon Cognito PKCE authorization URL.

    Returns dict with auth_url, state, and code_verifier.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN", "your-domain.auth.us-east-1.amazoncognito.com")
    client_id = os.environ.get("COGNITO_CLIENT_ID", "")

    if not client_id:
        raise ValueError("COGNITO_CLIENT_ID environment variable must be set")

    state = state or secrets.token_urlsafe(32)
    code_verifier, code_challenge = generate_pkce_pair()

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    auth_url = f"https://{cognito_domain}/oauth2/authorize?{urllib.parse.urlencode(params)}"

    return {
        "auth_url": auth_url,
        "state": state,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }


def exchange_pkce_code(
    code: str,
    redirect_uri: str,
    code_verifier: str,
    received_state: str,
    expected_state: str,
) -> dict:
    """
    Exchange an authorization code for tokens using PKCE with Amazon Cognito.

    Uses the Cognito Token endpoint to complete the PKCE flow.
    """
    if received_state != expected_state:
        raise ValueError("State mismatch: possible CSRF attack")

    cognito_domain = os.environ.get("COGNITO_DOMAIN", "your-domain.auth.us-east-1.amazoncognito.com")
    client_id = os.environ.get("COGNITO_CLIENT_ID", "")

    if not client_id:
        raise ValueError("COGNITO_CLIENT_ID environment variable must be set")

    token_url = f"https://{cognito_domain}/oauth2/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()
    token_response = response.json()

    return {
        "access_token": token_response.get("access_token"),
        "id_token": token_response.get("id_token"),
        "refresh_token": token_response.get("refresh_token"),
        "expires_in": token_response.get("expires_in"),
        "token_type": token_response.get("token_type", "Bearer"),
    }


def get_cognito_user_info(access_token: str) -> dict:
    """
    Fetch user information from Amazon Cognito User Pools using boto3.
    """
    client = boto3.client(
        "cognito-idp",
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )

    response = client.get_user(AccessToken=access_token)
    return response.get("UserAttributes", [])


def start_pkce_login(redirect_uri: str, scope: str = "") -> dict:
    """
    Full PKCE login initiation with Amazon Cognito.

    Returns the authorization URL along with PKCE parameters for callback.
    """
    result = build_pkce_auth_url(redirect_uri=redirect_uri, scope=scope)
    return {
        "provider": "amazon_cognito",
        "auth_url": result["auth_url"],
        "state": result["state"],
        "code_verifier": result["code_verifier"],
        "cognito_domain": os.environ.get("COGNITO_DOMAIN", ""),
    }
