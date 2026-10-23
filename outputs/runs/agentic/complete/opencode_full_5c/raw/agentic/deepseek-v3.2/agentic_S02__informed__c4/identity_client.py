import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class IdentityConfig:
    provider: str
    client_id: str
    client_secret: Optional[str] = None
    domain: Optional[str] = None
    tenant_id: Optional[str] = None
    redirect_uri: str = "http://localhost:3000/callback"
    scopes: str = "openid profile email"

    @classmethod
    def from_env(cls) -> "IdentityConfig":
        provider = os.environ.get("IDENTITY_PROVIDER", "auth0")

        if provider.lower() == "auth0":
            return cls(
                provider="auth0",
                client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
                client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
                domain=os.environ.get("AUTH0_DOMAIN", ""),
                redirect_uri=os.environ.get(
                    "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
                ),
                scopes=os.environ.get("AUTH0_SCOPES", "openid profile email"),
            )
        elif provider.lower() == "cognito":
            return cls(
                provider="cognito",
                client_id=os.environ.get("COGNITO_CLIENT_ID", ""),
                client_secret=os.environ.get("COGNITO_CLIENT_SECRET", ""),
                domain=os.environ.get("COGNITO_DOMAIN", ""),
                redirect_uri=os.environ.get(
                    "COGNITO_REDIRECT_URI", "http://localhost:3000/callback"
                ),
                scopes=os.environ.get("COGNITO_SCOPES", "openid profile email"),
            )
        elif provider.lower() == "azure":
            return cls(
                provider="azure",
                client_id=os.environ.get("AZURE_CLIENT_ID", ""),
                client_secret=os.environ.get("AZURE_CLIENT_SECRET", ""),
                tenant_id=os.environ.get("AZURE_TENANT_ID", ""),
                redirect_uri=os.environ.get(
                    "AZURE_REDIRECT_URI", "http://localhost:3000/callback"
                ),
                scopes=os.environ.get("AZURE_SCOPES", "openid profile email"),
            )
        else:
            raise ValueError(f"Unsupported identity provider: {provider}")


class IdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None):
        self.config = config or IdentityConfig.from_env()

    def get_authorization_endpoint(self) -> str:
        if self.config.provider == "auth0":
            return f"https://{self.config.domain}/authorize"
        elif self.config.provider == "cognito":
            return f"https://{self.config.domain}/oauth2/authorize"
        elif self.config.provider == "azure":
            return f"https://login.microsoftonline.com/{self.config.tenant_id}/oauth2/v2.0/authorize"
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    def get_token_endpoint(self) -> str:
        if self.config.provider == "auth0":
            return f"https://{self.config.domain}/oauth/token"
        elif self.config.provider == "cognito":
            return f"https://{self.config.domain}/oauth2/token"
        elif self.config.provider == "azure":
            return f"https://login.microsoftonline.com/{self.config.tenant_id}/oauth2/v2.0/token"
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    def get_userinfo_endpoint(self) -> str:
        if self.config.provider == "auth0":
            return f"https://{self.config.domain}/userinfo"
        elif self.config.provider == "cognito":
            return f"https://{self.config.domain}/oauth2/userInfo"
        elif self.config.provider == "azure":
            return "https://graph.microsoft.com/oidc/userinfo"
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    def validate_config(self) -> bool:
        required_fields = ["client_id", "redirect_uri"]

        for field in required_fields:
            if not getattr(self.config, field):
                return False

        if self.config.provider == "auth0" and not self.config.domain:
            return False
        elif self.config.provider == "cognito" and not self.config.domain:
            return False
        elif self.config.provider == "azure" and not self.config.tenant_id:
            return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self.config)


def load_identity_config() -> IdentityConfig:
    return IdentityConfig.from_env()


def create_identity_client() -> IdentityClient:
    return IdentityClient()
