# identity_client.py
# [HELPER] Local configuration and client helper utilities for Federated Login Flow

import os
from typing import Optional


class FederatedLoginConfig:
    """Encapsulates provider‑specific configuration loaded from environment variables."""

    def __init__(self, provider: str):
        self.provider = provider
        self.client_id = os.getenv(f"{provider.upper()}_CLIENT_ID")
        self.client_secret = os.getenv(f"{provider.upper()}_CLIENT_SECRET")
        self.redirect_uri = os.getenv(f"{provider.upper()}_REDIRECT_URI")
        self.default_scopes = os.getenv(
            f"{provider.upper()}_DEFAULT_SCOPES", "openid profile email"
        )

    @classmethod
    def from_env(cls, provider: str = None):
        """Instantiate config using the given provider or the default configured provider."""
        if provider is None:
            # Default provider can be set via env var DEFAULT_PROVIDER
            provider = os.getenv("DEFAULT_PROVIDER", "google")
        return cls(provider)

    def build_auth_url(
        self,
        client_id: str,
        redirect_uri: str,
        response_type: str,
        scope: str,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
    ) -> str:
        """Return a fully‑qualified authorization URL for the configured provider."""
        base = {
            "google": "https://accounts.google.com/o/oauth2/v2/auth",
            "okta": "https://{yourOktaDomain}/oauth2/default/v1/authorize",
            "azure_ad": "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize",
        }.get(self.provider.lower())
        if not base:
            raise ValueError(f"Unsupported provider for auth URL: {self.provider}")
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "scope": scope,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method,
        }
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v})
        return f"{base}?{query}"

    def get_user_profile(self, user_id: str):
        """Provider‑specific helper to fetch raw profile data.", raise NotImplementedError"""
        raise NotImplementedError("Subclasses must implement get_user_profile")

    def exchange_code_for_tokens(
        self,
        client_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
        scopes: str,
        code_verifier: Optional[str] = None,
    ):
        """Invoke the concrete provider client to exchange code for tokens.", raise NotImplementedError"""
        raise NotImplementedError("Subclasses must implement exchange_code_for_tokens")

    # \n    # Provider‑specific factory methods (example implementations for three providers)\n    # \n    @classmethod
    def from_env(cls, provider: str):
        if provider == "google":
            return GoogleClient(provider)
        elif provider == "okta":
            return OktaClient(provider)
        elif provider == "azure_ad":
            return AzureAdClient(provider)
        else:
            raise ValueError(f"Unknown provider: {provider}")


class GoogleClient(FederatedLoginConfig):
    def get_user_profile(self, user_id: str):
        # In a full implementation this would call Google's UserInfo endpoint
        raise NotImplementedError("Google profile fetching not implemented")

    def exchange_code_for_tokens(
        self,
        client_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
        scopes: str,
        code_verifier: Optional[str] = None,
    ):
        # Google's token exchange POST request
        raise NotImplementedError("Google token exchange not implemented")


class OktaClient(FederatedLoginConfig):
    def get_user_profile(self, user_id: str):
        # Okta's /userinfo endpoint request
        raise NotImplementedError("Okta profile fetching not implemented")

    def exchange_code_for_tokens(
        self,
        client_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
        scopes: str,
        code_verifier: Optional[str] = None,
    ):
        # Okta token exchange endpoint
        raise NotImplementedError("Okta token exchange not implemented")


class AzureAdClient(FederatedLoginConfig):
    def get_user_profile(self, user_id: str):
        # Azure AD UserInfo or Microsoft Graph call
        raise NotImplementedError("Azure AD profile fetching not implemented")

    def exchange_code_for_tokens(
        self,
        client_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
        scopes: str,
        code_verifier: Optional[str] = None,
    ):
        # Azure AD token endpoint request
        raise NotImplementedError("Azure AD token exchange not implemented")


class TokenSet:
    def __init__(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        id_token: Optional[str] = None,
        expires_at: Optional[int] = None,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_at = expires_at  # Unix epoch seconds (if known)

    def __repr__(self):
        return f"TokenSet(access={self.access_token}, refresh={self.refresh_token}, id={self.id_token})"


class TokenError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
