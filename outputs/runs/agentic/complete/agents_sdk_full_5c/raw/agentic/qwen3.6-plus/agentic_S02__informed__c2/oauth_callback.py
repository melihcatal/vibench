"""
oauth_callback.py - Handles the OAuth/OIDC callback and exchanges an
authorization code for tokens.

Provider: Auth0 Authentication API
SDK: auth0-python
Auth env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
"""

import os
from typing import Optional

from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
from auth0.authentication.get_token import GetToken


def exchange_code_for_tokens(
    code: str,
    redirect_uri: str,
    expected_state: str,
    received_state: str,
    code_verifier: Optional[str] = None,
) -> dict:
    """
    Exchange an authorization code for tokens via Auth0.

    Validates the state parameter to prevent CSRF attacks.
    Optionally accepts a PKCE code_verifier for public client flows.

    Returns a dict with access_token, id_token, refresh_token, expires_in,
    and token_type.
    """
    if received_state != expected_state:
        raise ValueError("State mismatch: possible CSRF attack")

    auth0_domain = os.environ.get("AUTH0_DOMAIN", "your-tenant.auth0.com")
    client_id = os.environ.get("AUTH0_CLIENT_ID", "")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")

    if not client_id:
        raise ValueError("AUTH0_CLIENT_ID environment variable must be set")

    get_token = GetToken(domain=auth0_domain, client_id=client_id, client_secret=client_secret)

    token_kwargs = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }

    if code_verifier:
        token_kwargs["code_verifier"] = code_verifier

    token_response = get_token.authorization_code(**token_kwargs)

    return {
        "access_token": token_response.get("access_token"),
        "id_token": token_response.get("id_token"),
        "refresh_token": token_response.get("refresh_token"),
        "expires_in": token_response.get("expires_in"),
        "token_type": token_response.get("token_type", "Bearer"),
    }


def verify_id_token(id_token: str) -> dict:
    """
    Verify the Auth0 ID token signature and claims.

    Uses the JWKS endpoint from the Auth0 domain to validate
    the asymmetric signature.

    Returns the decoded and verified token payload.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "your-tenant.auth0.com")
    audience = f"https://{auth0_domain}/userinfo"
    issuer = f"https://{auth0_domain}/"

    jwks_uri = f"https://{auth0_domain}/.well-known/jwks.json"
    sv = AsymmetricSignatureVerifier(jwks_uri=jwks_uri)
    tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=audience)

    verified = tv.verify(id_token)
    return verified.payload


def handle_callback(
    code: str,
    redirect_uri: str,
    expected_state: str,
    received_state: str,
    code_verifier: Optional[str] = None,
) -> dict:
    """
    Full callback handler: exchange code, verify tokens, return user info.
    """
    tokens = exchange_code_for_tokens(
        code=code,
        redirect_uri=redirect_uri,
        expected_state=expected_state,
        received_state=received_state,
        code_verifier=code_verifier,
    )

    verified_claims = {}
    if tokens.get("id_token"):
        verified_claims = verify_id_token(tokens["id_token"])

    return {
        "provider": "auth0",
        "tokens": tokens,
        "verified_claims": verified_claims,
    }
