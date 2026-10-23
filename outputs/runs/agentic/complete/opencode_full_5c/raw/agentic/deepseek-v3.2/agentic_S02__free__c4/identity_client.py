import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    scope: str
    provider: str


class IdentityClient:
    def __init__(self, provider: str = "google"):
        self.provider = provider
        self.config = self._load_config(provider)

    def _load_config(self, provider: str) -> OAuthConfig:
        if provider == "google":
            return OAuthConfig(
                client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
                client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get(
                    "GOOGLE_REDIRECT_URI", "http://localhost:8000/callback"
                ),
                authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
                token_endpoint="https://oauth2.googleapis.com/token",
                userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
                scope="openid email profile",
                provider="google",
            )
        elif provider == "github":
            return OAuthConfig(
                client_id=os.environ.get("GITHUB_CLIENT_ID", ""),
                client_secret=os.environ.get("GITHUB_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get(
                    "GITHUB_REDIRECT_URI", "http://localhost:8000/callback"
                ),
                authorization_endpoint="https://github.com/login/oauth/authorize",
                token_endpoint="https://github.com/login/oauth/access_token",
                userinfo_endpoint="https://api.github.com/user",
                scope="user:email",
                provider="github",
            )
        elif provider == "okta":
            okta_domain = os.environ.get("OKTA_DOMAIN", "")
            return OAuthConfig(
                client_id=os.environ.get("OKTA_CLIENT_ID", ""),
                client_secret=os.environ.get("OKTA_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get(
                    "OKTA_REDIRECT_URI", "http://localhost:8000/callback"
                ),
                authorization_endpoint=f"https://{okta_domain}/oauth2/default/v1/authorize",
                token_endpoint=f"https://{okta_domain}/oauth2/default/v1/token",
                userinfo_endpoint=f"https://{okta_domain}/oauth2/default/v1/userinfo",
                scope="openid profile email",
                provider="okta",
            )
        elif provider == "auth0":
            auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
            return OAuthConfig(
                client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
                client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get(
                    "AUTH0_REDIRECT_URI", "http://localhost:8000/callback"
                ),
                authorization_endpoint=f"https://{auth0_domain}/authorize",
                token_endpoint=f"https://{auth0_domain}/oauth/token",
                userinfo_endpoint=f"https://{auth0_domain}/userinfo",
                scope="openid profile email",
                provider="auth0",
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_config_dict(self) -> Dict[str, Any]:
        return asdict(self.config)

    def validate_config(self) -> bool:
        required_fields = ["client_id", "client_secret"]

        for field in required_fields:
            if not getattr(self.config, field):
                return False

        if self.provider in ["okta", "auth0"]:
            if self.provider == "okta" and not os.environ.get("OKTA_DOMAIN"):
                return False
            if self.provider == "auth0" and not os.environ.get("AUTH0_DOMAIN"):
                return False

        return True

    def get_scopes(self) -> list:
        return self.config.scope.split()

    def add_custom_scope(self, scope: str):
        if scope not in self.config.scope:
            self.config.scope = f"{self.config.scope} {scope}"

    @staticmethod
    def list_available_providers() -> list:
        return ["google", "github", "okta", "auth0", "azure_ad", "cognito"]
