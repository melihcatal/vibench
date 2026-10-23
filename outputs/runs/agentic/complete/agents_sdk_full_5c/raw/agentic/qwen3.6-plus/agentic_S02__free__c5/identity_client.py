"""
Local configuration and client helper utilities for Federated Login Flow.
Provides OAuth2/OIDC client setup, environment loading, and request helpers.
"""

import os
import base64
import hashlib
import secrets
import string
from urllib.parse import urlencode, urlparse
from typing import Optional, Dict, Any

import httpx


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "dev-example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:3000/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"


class OAuthClient:
    """Helper for constructing Auth0 OAuth2/OIDC requests."""

    def __init__(
        self,
        domain: str = AUTH0_DOMAIN,
        client_id: str = AUTH0_CLIENT_ID,
        client_secret: str = AUTH0_CLIENT_SECRET,
        redirect_uri: str = AUTH0_REDIRECT_URI,
        audience: str = AUTH0_AUDIENCE,
    ):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.audience = audience
        self.base_url = f"https://{self.domain}"

    def authorize_url(
        self,
        state: str,
        scope: str = "openid profile email",
        response_type: str = "code",
        extra_params: Optional[Dict[str, str]] = None,
    ) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": response_type,
            "scope": scope,
            "state": state,
        }
        if self.audience:
            params["audience"] = self.audience
        if extra_params:
            params.update(extra_params)
        return f"{self.base_url}/authorize?{urlencode(params)}"

    def token_url(self) -> str:
        return f"{self.base_url}/oauth/token"

    def userinfo_url(self) -> str:
        return f"{self.base_url}/userinfo"

    def jwks_url(self) -> str:
        return f"{self.base_url}/.well-known/jwks.json"

    def openid_config_url(self) -> str:
        return f"{self.base_url}/.well-known/openid-configuration"

    async def exchange_code(
        self,
        code: str,
        code_verifier: Optional[str] = None,
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            payload = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
            }
            if code_verifier:
                payload["code_verifier"] = code_verifier
            response = await client.post(self.token_url(), data=payload)
            response.raise_for_status()
            return response.json()

    async def get_userinfo(self, access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(self.userinfo_url(), headers=headers)
            response.raise_for_status()
            return response.json()


def generate_state(length: int = 32) -> str:
    """Generate a cryptographically secure state parameter."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_code_verifier(length: int = 64) -> str:
    """Generate a PKCE code verifier per RFC 7636."""
    alphabet = string.ascii_letters + string.digits + "-._~"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_code_challenge(code_verifier: str, method: str = "S256") -> str:
    """Generate a PKCE code challenge from a verifier."""
    if method == "S256":
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return code_verifier


def create_auth0_client(
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    audience: Optional[str] = None,
) -> OAuthClient:
    """Factory to create an Auth0 OAuthClient with overrides."""
    return OAuthClient(
        domain=domain or AUTH0_DOMAIN,
        client_id=client_id or AUTH0_CLIENT_ID,
        client_secret=client_secret or AUTH0_CLIENT_SECRET,
        redirect_uri=redirect_uri or AUTH0_REDIRECT_URI,
        audience=audience or AUTH0_AUDIENCE,
    )
