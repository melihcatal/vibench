from typing import Optional, Dict, Any
import os
import json
import requests
from jose import jwt
from jose.exceptions import JWTError


class OAuthConfig:
    def __init__(self):
        self.idaas_issuer = os.getenv("ALIBABA_IDAAS_ISSUER")
        self.client_id = os.getenv("ALIBABA_IDAAS_CLIENT_ID")
        self.redirect_uri = os.getenv(
            "ALIBABA_IDAAS_REDIRECT_URI", "http://localhost:8000/callback"
        )
        self.scope = os.getenv("ALIBABA_IDAAS_SCOPE", "openid profile email")
        self.auth_url = f"{self.idaas_issuer}/oauth2/v1/authorize"
        self.token_url = f"{self.idaas_issuer}/oauth2/v1/token"
        self.jwks_url = f"{self.idaas_issuer}/oauth2/v1/jwks"
        self.client_secret = os.getenv("ALIBABA_IDAAS_CLIENT_SECRET")


class OAuthClient:
    def __init__(self, config: OAuthConfig):
        self.config = config
        self.jwks = self._fetch_jwks()

    def _fetch_jwks(self) -> Dict[str, Any]:
        response = requests.get(self.config.jwks_url)
        response.raise_for_status()
        return response.json()

    def validate_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self.jwks,
                algorithms=["RS256"],
                audience=self.config.client_id,
                issuer=self.config.idaas_issuer,
            )
        except JWTError as e:
            raise ValueError(f"Invalid token: {e}")


class PKCEHelper:
    @staticmethod
    def generate_code_verifier() -> str:
        import secrets

        return secrets.token_urlsafe(64)

    @staticmethod
    def generate_code_challenge(verifier: str) -> str:
        import hashlib
        import base64

        challenge = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(challenge).decode().replace("=", "")


class OAuthResponse:
    def __init__(
        self,
        access_token: str,
        id_token: str,
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None,
    ):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in


class OAuthError:
    def __init__(self, error: str, error_description: Optional[str] = None):
        self.error = error
        self.error_description = error_description
