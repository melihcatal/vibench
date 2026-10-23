import os
import json
from typing import Dict, Any, Optional
from enum import Enum


class IdentityProvider(Enum):
    AUTH0 = "auth0"
    COGNITO = "cognito"
    AZURE_AD = "azure_ad"
    GOOGLE = "google"


class IdentityClientConfig:
    """Configuration for identity provider clients."""

    def __init__(self, provider: IdentityProvider):
        self.provider = provider
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}

        if self.provider == IdentityProvider.AUTH0:
            config.update(
                {
                    "domain": os.environ.get("AUTH0_DOMAIN"),
                    "client_id": os.environ.get("AUTH0_CLIENT_ID"),
                    "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
                    "audience": os.environ.get("AUTH0_AUDIENCE"),
                    "scope": os.environ.get("AUTH0_SCOPE", "openid profile email"),
                }
            )

        elif self.provider == IdentityProvider.COGNITO:
            config.update(
                {
                    "domain": os.environ.get("COGNITO_DOMAIN"),
                    "client_id": os.environ.get("COGNITO_CLIENT_ID"),
                    "client_secret": os.environ.get("COGNITO_CLIENT_SECRET"),
                    "user_pool_id": os.environ.get("COGNITO_USER_POOL_ID"),
                    "region": os.environ.get("COGNITO_REGION"),
                    "scope": os.environ.get("COGNITO_SCOPE", "openid profile email"),
                }
            )

        elif self.provider == IdentityProvider.AZURE_AD:
            config.update(
                {
                    "tenant_id": os.environ.get("AZURE_TENANT_ID"),
                    "client_id": os.environ.get("AZURE_CLIENT_ID"),
                    "client_secret": os.environ.get("AZURE_CLIENT_SECRET"),
                    "authority": os.environ.get("AZURE_AUTHORITY"),
                    "scope": os.environ.get("AZURE_SCOPE", "openid profile email"),
                }
            )

        elif self.provider == IdentityProvider.GOOGLE:
            config.update(
                {
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                    "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
                    "scope": os.environ.get("GOOGLE_SCOPE", "openid profile email"),
                }
            )

        return config

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if self.provider == IdentityProvider.AUTH0:
            required = ["domain", "client_id"]
        elif self.provider == IdentityProvider.COGNITO:
            required = ["domain", "client_id"]
        elif self.provider == IdentityProvider.AZURE_AD:
            required = ["tenant_id", "client_id"]
        elif self.provider == IdentityProvider.GOOGLE:
            required = ["client_id"]
        else:
            return False

        return all(self.config.get(key) for key in required)

    def get_redirect_uri(self, base_url: str = None) -> str:
        """Get the redirect URI for this provider."""
        if base_url:
            return f"{base_url}/auth/callback/{self.provider.value}"

        # Fallback to environment variable or default
        redirect_uri = os.environ.get(f"{self.provider.name}_REDIRECT_URI")
        if not redirect_uri:
            raise ValueError(f"Redirect URI not configured for {self.provider.value}")

        return redirect_uri


class IdentityClient:
    """Client helper for identity provider operations."""

    def __init__(self, provider: IdentityProvider):
        self.provider = provider
        self.config = IdentityClientConfig(provider)

        if not self.config.validate():
            raise ValueError(f"Invalid configuration for {provider.value}")

    def get_authorization_url(
        self, redirect_uri: str = None, state: str = None, use_pkce: bool = False
    ) -> str:
        """Get authorization URL for the identity provider."""
        from start_oauth_login import start_auth0_oauth_login, start_cognito_oauth_login
        from pkce_login import start_auth0_pkce_login, start_cognito_pkce_login

        if not redirect_uri:
            redirect_uri = self.config.get_redirect_uri()

        if self.provider == IdentityProvider.AUTH0:
            if use_pkce:
                auth_url, _ = start_auth0_pkce_login(
                    redirect_uri, state, self.config.config.get("scope")
                )
                return auth_url
            else:
                return start_auth0_oauth_login(
                    redirect_uri, state, self.config.config.get("scope")
                )

        elif self.provider == IdentityProvider.COGNITO:
            if use_pkce:
                auth_url, _ = start_cognito_pkce_login(
                    redirect_uri, state, self.config.config.get("scope")
                )
                return auth_url
            else:
                return start_cognito_oauth_login(
                    redirect_uri, state, self.config.config.get("scope")
                )

        raise NotImplementedError(f"Provider {self.provider.value} not implemented")

    def exchange_code_for_tokens(
        self,
        authorization_code: str,
        redirect_uri: str = None,
        code_verifier: str = None,
    ) -> Dict[str, Any]:
        """Exchange authorization code for tokens."""
        from oauth_callback import (
            exchange_auth0_code_for_tokens,
            exchange_cognito_code_for_tokens,
        )
        from pkce_login import (
            exchange_auth0_pkce_code_for_tokens,
            exchange_cognito_pkce_code_for_tokens,
        )

        if not redirect_uri:
            redirect_uri = self.config.get_redirect_uri()

        if self.provider == IdentityProvider.AUTH0:
            if code_verifier:
                return exchange_auth0_pkce_code_for_tokens(
                    authorization_code, code_verifier, redirect_uri
                )
            else:
                return exchange_auth0_code_for_tokens(authorization_code, redirect_uri)

        elif self.provider == IdentityProvider.COGNITO:
            if code_verifier:
                return exchange_cognito_pkce_code_for_tokens(
                    authorization_code, code_verifier, redirect_uri
                )
            else:
                return exchange_cognito_code_for_tokens(
                    authorization_code, redirect_uri
                )

        raise NotImplementedError(f"Provider {self.provider.value} not implemented")

    def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """Get user profile from identity provider."""
        from profile_claims import (
            fetch_auth0_user_profile,
            fetch_cognito_user_profile,
            normalize_user_profile,
        )

        if self.provider == IdentityProvider.AUTH0:
            raw_profile = fetch_auth0_user_profile(access_token)
            return normalize_user_profile(raw_profile, "auth0")

        elif self.provider == IdentityProvider.COGNITO:
            raw_profile = fetch_cognito_user_profile(access_token)
            return normalize_user_profile(raw_profile, "cognito")

        raise NotImplementedError(f"Provider {self.provider.value} not implemented")
