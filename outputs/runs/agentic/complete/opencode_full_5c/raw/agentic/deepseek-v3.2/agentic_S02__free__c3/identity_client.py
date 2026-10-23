import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    auth_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    scope: str = "openid profile email"

    @classmethod
    def from_google(cls):
        return cls(
            client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            redirect_uri=os.environ.get(
                "GOOGLE_REDIRECT_URI", "http://localhost:5000/callback"
            ),
            auth_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
            token_endpoint="https://oauth2.googleapis.com/token",
            userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
            scope="openid email profile",
        )

    @classmethod
    def from_okta(cls):
        okta_domain = os.environ.get("OKTA_DOMAIN", "https://dev-123456.okta.com")
        return cls(
            client_id=os.environ.get("OKTA_CLIENT_ID", ""),
            client_secret=os.environ.get("OKTA_CLIENT_SECRET", ""),
            redirect_uri=os.environ.get(
                "OKTA_REDIRECT_URI", "http://localhost:5000/pkce-callback"
            ),
            auth_endpoint=f"{okta_domain}/oauth2/default/v1/authorize",
            token_endpoint=f"{okta_domain}/oauth2/default/v1/token",
            userinfo_endpoint=f"{okta_domain}/oauth2/default/v1/userinfo",
            scope="openid profile email",
        )


class IdentityClient:
    def __init__(self, provider: str = "google"):
        self.provider = provider
        if provider == "google":
            self.config = OAuthConfig.from_google()
        elif provider == "okta":
            self.config = OAuthConfig.from_okta()
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_auth_url(
        self, state: str, nonce: str, code_challenge: Optional[str] = None
    ) -> str:
        from urllib.parse import urlencode

        params = {
            "client_id": self.config.client_id,
            "response_type": "code",
            "redirect_uri": self.config.redirect_uri,
            "scope": self.config.scope,
            "state": state,
            "nonce": nonce,
        }

        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"

        return f"{self.config.auth_endpoint}?{urlencode(params)}"

    def validate_config(self) -> bool:
        required_fields = ["client_id", "client_secret", "redirect_uri"]
        for field in required_fields:
            if not getattr(self.config, field):
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "config": asdict(self.config),
            "is_valid": self.validate_config(),
        }


def load_identity_config() -> Dict[str, Any]:
    configs = {}

    google_config = OAuthConfig.from_google()
    if google_config.client_id and google_config.client_secret:
        configs["google"] = asdict(google_config)

    okta_config = OAuthConfig.from_okta()
    if okta_config.client_id and okta_config.client_secret:
        configs["okta"] = asdict(okta_config)

    return configs
