import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class IdentityProvider(Enum):
    AUTH0 = "auth0"
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    COGNITO = "cognito"


@dataclass
class AuthConfig:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scopes: Optional[str] = None

    @classmethod
    def from_env(cls, provider: IdentityProvider = IdentityProvider.AUTH0):
        if provider == IdentityProvider.AUTH0:
            return cls(
                domain=os.environ.get("AUTH0_DOMAIN", ""),
                client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
                client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get(
                    "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
                ),
                scopes=os.environ.get("AUTH0_SCOPES", "openid profile email"),
            )
        elif provider == IdentityProvider.GOOGLE:
            return cls(
                domain="accounts.google.com",
                client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
                client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
                redirect_uri=os.environ.get("GOOGLE_REDIRECT_URI", ""),
                scopes=os.environ.get("GOOGLE_SCOPES", "openid profile email"),
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")


class IdentityClient:
    def __init__(self, provider: IdentityProvider = IdentityProvider.AUTH0):
        self.provider = provider
        self.config = AuthConfig.from_env(provider)
        self._validate_config()

    def _validate_config(self):
        if not self.config.domain:
            raise ValueError(f"{self.provider.value.upper()}_DOMAIN is required")
        if not self.config.client_id:
            raise ValueError(f"{self.provider.value.upper()}_CLIENT_ID is required")

    def get_auth_url(self, state: str, nonce: str, use_pkce: bool = False) -> str:
        base_url = f"https://{self.config.domain}/authorize"

        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": self.config.scopes,
            "state": state,
            "nonce": nonce,
        }

        if use_pkce:
            from pkce_login import generate_pkce_verifier, generate_pkce_challenge

            verifier = generate_pkce_verifier()
            challenge = generate_pkce_challenge(verifier)
            params["code_challenge"] = challenge
            params["code_challenge_method"] = "S256"
            return base_url, params, verifier

        return base_url, params, None

    def exchange_code(
        self, auth_code: str, code_verifier: Optional[str] = None
    ) -> Dict[str, Any]:
        token_url = f"https://{self.config.domain}/oauth/token"

        payload = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": auth_code,
            "redirect_uri": self.config.redirect_uri,
        }

        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret

        if code_verifier:
            payload["code_verifier"] = code_verifier

        import requests

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(token_url, data=payload, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Token exchange failed: {response.text}")

        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        userinfo_url = f"https://{self.config.domain}/userinfo"

        import requests

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(userinfo_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user info: {response.text}")

        return response.json()
