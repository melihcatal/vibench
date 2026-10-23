"""
Local configuration and client helper utilities for Federated Login Flow.

Provider: Auth0 Authentication API
Environment variables: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET,
                       AUTH0_CALLBACK_URL, AUTH0_SCOPE
"""

import os
import base64
import hashlib
import secrets
from typing import Optional
from urllib.parse import urlencode, urljoin


class Auth0Config:
    """Configuration holder for Auth0 OIDC integration."""

    def __init__(
        self,
        domain: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        callback_url: Optional[str] = None,
        scope: Optional[str] = None,
    ):
        self.domain = domain or os.environ.get("AUTH0_DOMAIN", "")
        self.client_id = client_id or os.environ.get("AUTH0_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("AUTH0_CLIENT_SECRET", "")
        self.callback_url = callback_url or os.environ.get(
            "AUTH0_CALLBACK_URL", "http://localhost:8080/callback"
        )
        self.scope = scope or os.environ.get(
            "AUTH0_SCOPE", "openid profile email"
        )

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}/"

    @property
    def authorization_endpoint(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.domain}/userinfo"

    @property
    def jwks_uri(self) -> str:
        return f"https://{self.domain}/.well-known/jwks.json"

    @property
    def logout_endpoint(self) -> str:
        return f"https://{self.domain}/v2/logout"

    def is_configured(self) -> bool:
        return bool(self.domain and self.client_id)


def generate_state(length: int = 32) -> str:
    """Generate a cryptographically secure state parameter."""
    return secrets.token_urlsafe(length)


def generate_nonce(length: int = 32) -> str:
    """Generate a cryptographically secure nonce parameter."""
    return secrets.token_urlsafe(length)


def generate_code_verifier(length: int = 64) -> str:
    """Generate a PKCE code_verifier as per RFC 7636."""
    token = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(token).rstrip(b"=").decode("ascii")


def generate_code_challenge(code_verifier: str, method: str = "S256") -> str:
    """Generate a PKCE code_challenge from a code_verifier."""
    if method == "S256":
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return code_verifier


def build_auth_url(
    config: Auth0Config,
    state: str,
    nonce: str,
    redirect_uri: Optional[str] = None,
    response_type: str = "code",
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
    connection: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> str:
    """Build the Auth0 authorization URL."""
    params = {
        "client_id": config.client_id,
        "redirect_uri": redirect_uri or config.callback_url,
        "response_type": response_type,
        "scope": config.scope,
        "state": state,
        "nonce": nonce,
    }

    if code_challenge:
        params["code_challenge"] = code_challenge
    if code_challenge_method:
        params["code_challenge_method"] = code_challenge_method
    if connection:
        params["connection"] = connection
    if extra_params:
        params.update(extra_params)

    query = urlencode(params)
    return f"{config.authorization_endpoint}?{query}"


def build_logout_url(
    config: Auth0Config,
    return_to: Optional[str] = None,
    client_id: Optional[str] = None,
) -> str:
    """Build the Auth0 logout URL."""
    params = {
        "returnTo": return_to or config.callback_url,
        "client_id": client_id or config.client_id,
    }
    query = urlencode(params)
    return f"{config.logout_endpoint}?{query}"


def get_config() -> Auth0Config:
    """Load Auth0 configuration from environment variables."""
    return Auth0Config()
