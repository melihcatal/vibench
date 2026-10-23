import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: list
    provider: str


class IdentityClient:
    def __init__(self, provider: str = "google"):
        self.provider = provider
        self.config = self._load_config(provider)

    def _load_config(self, provider: str) -> OAuthConfig:
        if provider == "google":
            return OAuthConfig(
                client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID", ""),
                client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get(
                    "GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8000/callback"
                ),
                scopes=["openid", "email", "profile"],
                provider="google",
            )
        elif provider == "okta":
            return OAuthConfig(
                client_id=os.environ.get("OKTA_OAUTH_CLIENT_ID", ""),
                client_secret=os.environ.get("OKTA_OAUTH_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get(
                    "OKTA_OAUTH_REDIRECT_URI", "http://localhost:8000/callback"
                ),
                scopes=["openid", "profile", "email"],
                provider="okta",
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_endpoints(self) -> Dict[str, str]:
        if self.provider == "google":
            return {
                "authorization": "https://accounts.google.com/o/oauth2/v2/auth",
                "token": "https://oauth2.googleapis.com/token",
                "userinfo": "https://openidconnect.googleapis.com/v1/userinfo",
                "jwks": "https://www.googleapis.com/oauth2/v3/certs",
            }
        elif self.provider == "okta":
            domain = os.environ.get("OKTA_DOMAIN", "https://dev-123456.okta.com")
            return {
                "authorization": f"{domain}/oauth2/default/v1/authorize",
                "token": f"{domain}/oauth2/default/v1/token",
                "userinfo": f"{domain}/oauth2/default/v1/userinfo",
                "jwks": f"{domain}/oauth2/default/v1/keys",
            }
        else:
            return {}

    def validate_config(self) -> bool:
        required_vars = ["client_id", "client_secret", "redirect_uri"]
        for var in required_vars:
            if not getattr(self.config, var):
                return False
        return True
