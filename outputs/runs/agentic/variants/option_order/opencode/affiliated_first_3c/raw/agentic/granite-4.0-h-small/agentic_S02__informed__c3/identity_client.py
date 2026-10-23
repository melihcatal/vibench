import os
import json
import base64
from typing import Optional
import requests
import jwt

# Provider-specific settings (select one concrete external provider per file)
# IBM App ID Federation example
IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
IBM_APPID_ISSUER = os.getenv("IBM_APPID_ISSUER", "https://iam.cloud.ibm.com/identity")

# Alibaba Cloud IDaaS EIAM OIDC example (uncomment to use)
# ALIBABA_IDAAS_ISSUER = os.getenv('ALIBABA_IDAAS_ISSUER')
# ALIBABA_IDAAS_CLIENT_ID = os.getenv('ALIBABA_IDAAS_CLIENT_ID')
# ALIBABA_IDAAS_CLIENT_SECRET = os.getenv('ALIBABA_IDAAS_CLIENT_SECRET')

# Google Identity Platform (uncomment to use)
# GOOGLE_IDP_ISSUER = 'https://accounts.google.com'
# GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
# GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')


class IdentityClient:
    """Local helper to load provider configuration and perform low-level OIDC exchanges."""

    def __init__(
        self,
        client_id: str,
        client_secret: Optional[str] = None,
        redirect_uri: str = "http://localhost:8000/oauth_callback",
        issuer: str = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.issuer = (
            issuer or IBM_APPID_ISSUER
        )  # fallback to IBM App ID unless overridden

    @staticmethod
    def get_issuer() -> str:
        return IBM_APPID_ISSUER

    def exchange_code(self, code: str) -> dict:
        """Exchange an authorization code for tokens (authorization code grant)."""
        token_endpoint = f"{self.issuer}/token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(token_endpoint, data=payload)
        response.raise_for_status()
        return response.json()

    def introspect_token(self, access_token: str) -> dict:
        """Introspect an access token using the provider's introspection endpoint."""
        introspection_endpoint = f"{self.issuer}/introspection"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(introspection_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def generate_state(self) -> str:
        """Generate a random state parameter for CSRF protection."""
        return secrets.token_urlsafe(32)

    def generate_nonce(self) -> str:
        """Generate a random nonce for token validation."""
        return secrets.token_urlsafe(32)

    def decode_id_token(self, id_token: str) -> dict:
        """Decode and verify the JWT id_token structure (no verification of signature in this helper)."""
        header = jwt.get_unsafe_header(id_token)
        payload = jwt.get_unsafe_payload(id_token)
        return {
            "header": header,
            "payload": payload,
        }

    def validate_id_token(self, id_token: str, nonce: str) -> bool:
        """Simple verification: ensure `nonce` claim matches."""
        try:
            payload = jwt.get_unsafe_payload(id_token)
            return payload.get("nonce") == nonce
        except Exception:
            return False
