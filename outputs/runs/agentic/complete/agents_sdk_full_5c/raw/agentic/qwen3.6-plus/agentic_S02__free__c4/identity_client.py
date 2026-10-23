"""
Local configuration and client helper utilities for Federated Login Flow.

Provides OAuth/OIDC client configuration, HTTP session management,
and PKCE parameter helpers for identity provider integrations.
"""

import os
import json
import base64
import hashlib
import secrets
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class ProviderType(str, Enum):
    """Supported identity provider types."""
    OKTA = "okta"
    AUTH0 = "auth0"
    GOOGLE = "google"
    AZURE_AD = "azure_ad"


@dataclass
class OAuthConfig:
    """OAuth/OIDC client configuration."""
    provider: ProviderType
    client_id: str
    client_secret: Optional[str] = None
    issuer: str = ""
    authorize_url: str = ""
    token_url: str = ""
    userinfo_url: str = ""
    jwks_url: str = ""
    redirect_uri: str = ""
    scope: str = "openid profile email"
    audience: Optional[str] = None
    timeout: int = 30


@dataclass
class PKCESession:
    """PKCE flow session state."""
    session_id: str
    code_verifier: str
    code_challenge: str
    state: str
    nonce: str
    created_at: int = field(default_factory=lambda: int(time.time()))
    expires_at: int = field(default=0)

    def __post_init__(self):
        if not self.expires_at:
            self.expires_at = self.created_at + 600  # 10 minute expiry

    def is_expired(self) -> bool:
        return int(time.time()) > self.expires_at


def load_config_from_env(provider: ProviderType = ProviderType.OKTA) -> OAuthConfig:
    """Load OAuth configuration from environment variables."""
    if provider == ProviderType.OKTA:
        org_url = os.getenv("OKTA_ORG_URL", "https://dev-123456.okta.com")
        auth_server = os.getenv("OKTA_AUTH_SERVER_ID", "default")
        return OAuthConfig(
            provider=ProviderType.OKTA,
            client_id=os.getenv("OKTA_CLIENT_ID", ""),
            client_secret=os.getenv("OKTA_CLIENT_SECRET"),
            issuer=f"{org_url}/oauth2/{auth_server}",
            authorize_url=f"{org_url}/oauth2/{auth_server}/v1/authorize",
            token_url=f"{org_url}/oauth2/{auth_server}/v1/token",
            userinfo_url=f"{org_url}/oauth2/{auth_server}/v1/userinfo",
            jwks_url=f"{org_url}/oauth2/{auth_server}/v1/keys",
            redirect_uri=os.getenv("OKTA_REDIRECT_URI", "https://app.example.com/callback"),
            scope=os.getenv("OKTA_SCOPE", "openid profile email"),
        )
    elif provider == ProviderType.AUTH0:
        domain = os.getenv("AUTH0_DOMAIN", "dev-example.us.auth0.com")
        return OAuthConfig(
            provider=ProviderType.AUTH0,
            client_id=os.getenv("AUTH0_CLIENT_ID", ""),
            client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
            issuer=f"https://{domain}/",
            authorize_url=f"https://{domain}/authorize",
            token_url=f"https://{domain}/oauth/token",
            userinfo_url=f"https://{domain}/userinfo",
            jwks_url=f"https://{domain}/.well-known/jwks.json",
            redirect_uri=os.getenv("AUTH0_REDIRECT_URI", "https://app.example.com/callback"),
            scope=os.getenv("AUTH0_SCOPE", "openid profile email"),
            audience=os.getenv("AUTH0_AUDIENCE"),
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def load_config_from_file(path: str = "oauth_config.json") -> OAuthConfig:
    """Load OAuth configuration from JSON file."""
    with open(path, "r") as f:
        data = json.load(f)

    provider = ProviderType(data.get("provider", "okta"))
    return OAuthConfig(
        provider=provider,
        client_id=data["client_id"],
        client_secret=data.get("client_secret"),
        issuer=data.get("issuer", ""),
        authorize_url=data.get("authorize_url", ""),
        token_url=data.get("token_url", ""),
        userinfo_url=data.get("userinfo_url", ""),
        jwks_url=data.get("jwks_url", ""),
        redirect_uri=data.get("redirect_uri", ""),
        scope=data.get("scope", "openid profile email"),
        audience=data.get("audience"),
        timeout=data.get("timeout", 30),
    )


def generate_pkce_parameters(
    code_verifier_length: int = 64,
) -> Dict[str, str]:
    """
    Generate PKCE code_verifier and code_challenge.

    code_challenge = BASE64URL(SHA256(code_verifier)) per RFC 7636.
    """
    code_verifier = secrets.token_urlsafe(code_verifier_length)[:code_verifier_length]
    sha256_hash = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_hash).rstrip(b"=").decode("ascii")

    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }


def get_pkce_config(provider: ProviderType = ProviderType.AUTH0) -> dict:
    """Get PKCE-specific configuration for a provider."""
    if provider == ProviderType.AUTH0:
        return {
            "provider": "auth0",
            "code_challenge_method": "S256",
            "requires_code_verifier": True,
            "supports_client_secret": False,
            "token_url": f"https://{os.getenv('AUTH0_DOMAIN', 'dev-example.us.auth0.com')}/oauth/token",
        }
    elif provider == ProviderType.OKTA:
        return {
            "provider": "okta",
            "code_challenge_method": "S256",
            "requires_code_verifier": True,
            "supports_client_secret": True,
            "token_url": f"{os.getenv('OKTA_ORG_URL', 'https://dev-123456.okta.com')}/oauth2/{os.getenv('OKTA_AUTH_SERVER_ID', 'default')}/v1/token",
        }
    else:
        return {
            "provider": provider.value,
            "code_challenge_method": "S256",
            "requires_code_verifier": True,
            "supports_client_secret": False,
        }


def build_auth_headers(access_token: str, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Build authorization headers for OIDC API calls."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    return headers


def validate_token_response(response_data: Dict[str, Any]) -> bool:
    """Validate that token response contains required fields."""
    required_fields = {"access_token", "token_type", "expires_in"}
    return required_fields.issubset(set(response_data.keys()))


def get_default_timeout(config: Optional[OAuthConfig] = None) -> int:
    """Get default HTTP timeout for identity provider calls."""
    if config:
        return config.timeout
    return int(os.getenv("IDENTITY_HTTP_TIMEOUT", "30"))
