"""
Local configuration and client helper utilities for Federated Login Flow.

Provides an IdentityClient wrapper for managing connections to Auth0
including token handling, profile retrieval, and user info endpoints.
"""

import json
import os
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests


# Auth0-specific configuration defaults
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.environ.get(
    "AUTH0_REDIRECT_URI", "http://localhost:8080/callback"
)
AUTH0_AUDIENCE = os.environ.get(
    "AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/"
)

# Auth0 well-known endpoints
AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}"
AUTH0_AUTHORIZE_URL = f"{AUTH0_BASE_URL}/authorize"
AUTH0_TOKEN_URL = f"{AUTH0_BASE_URL}/oauth/token"
AUTH0_USERINFO_URL = f"{AUTH0_BASE_URL}/userinfo"
AUTH0_OIDC_CONFIG_URL = f"{AUTH0_BASE_URL}/.well-known/openid-configuration"
AUTH0_LOGOUT_URL = f"{AUTH0_BASE_URL}/v2/logout"


class IdentityClient:
    """
    Helper client for interacting with Auth0's OAuth 2.0 / OIDC endpoints.

    Provides methods for token exchange, user info retrieval, and
    configuration discovery against a concrete Auth0 tenant.
    """

    def __init__(
        self,
        domain: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        audience: Optional[str] = None,
    ):
        self.domain = domain or AUTH0_DOMAIN
        self.client_id = client_id or AUTH0_CLIENT_ID
        self.client_secret = client_secret or AUTH0_CLIENT_SECRET
        self.redirect_uri = redirect_uri or AUTH0_REDIRECT_URI
        self.audience = audience or AUTH0_AUDIENCE
        self.base_url = f"https://{self.domain}"
        self.session = requests.Session()
        self._oidc_config: Optional[Dict[str, Any]] = None

    @property
    def authorize_url(self) -> str:
        return f"{self.base_url}/authorize"

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"{self.base_url}/userinfo"

    def fetch_oidc_configuration(self) -> Dict[str, Any]:
        """
        Fetch the Auth0 OpenID Connect discovery document from
        .well-known/openid-configuration.
        """
        if self._oidc_config is not None:
            return self._oidc_config

        resp = self.session.get(
            f"{self.base_url}/.well-known/openid-configuration",
            timeout=10,
        )
        resp.raise_for_status()
        self._oidc_config = resp.json()
        return self._oidc_config

    def exchange_authorization_code(
        self,
        code: str,
        code_verifier: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Exchange an authorization code for tokens at the Auth0 /oauth/token
        endpoint.

        Auth0 requires grant_type=authorization_code with the Auth0-issued
        client credentials in the request body.
        """
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        if code_verifier:
            payload["code_verifier"] = code_verifier

        resp = self.session.post(
            self.token_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Fetch the authenticated user's profile from the Auth0 /userinfo
        endpoint using a valid access token.
        """
        resp = self.session.get(
            self.userinfo_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def introspect_token(self, token: str, token_type_hint: str = "access_token") -> Dict[str, Any]:
        """
        Introspect an Auth0 access or refresh token via the
        /oauth/introspect endpoint.
        """
        payload = {
            "token": token,
            "token_type_hint": token_type_hint,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        resp = self.session.post(
            f"{self.base_url}/oauth/introspect",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Request new tokens from Auth0 using a refresh token.
        """
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }
        resp = self.session.post(
            self.token_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()

    def revoke_token(self, token: str) -> bool:
        """
        Revoke an Auth0 token via the /oauth/revoke endpoint.
        """
        payload = {
            "token": token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        resp = self.session.post(
            f"{self.base_url}/oauth/revoke",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.status_code == 200

    def build_logout_url(self, return_to: Optional[str] = None) -> str:
        """
        Build an Auth0 logout URL. Auth0's /v2/logout endpoint accepts
        client_id and returnTo query parameters.
        """
        params = {"client_id": self.client_id}
        if return_to:
            params["returnTo"] = return_to
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.base_url}/v2/logout?{qs}"

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()

    def __enter__(self) -> "IdentityClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
