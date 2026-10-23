import os
import json
import urllib.parse
import urllib.request
import ssl
from typing import Dict, Any, Optional


class IdentityClient:
    """Local helper for Alibaba Cloud IDaaS EIAM OIDC integration."""

    def __init__(self):
        # Environment variables for Alibaba IDaaS configuration
        self.issuer = os.getenv("ALIBABA_IDAAS_ISSUER")
        self.client_id = os.getenv("ALIBABA_IDAAS_CLIENT_ID")
        self.redirect_uri = os.getenv("ALIBABA_IDAAS_REDIRECT_URI")
        # PKCE: store verifier during login flow (for verification after callback)
        self._code_verifier: Optional[str] = None

        # Simple in‑memory token cache (optional)
        self._tokens: Dict[str, Any] = {}

    def generate_state(self, length=32) -> str:
        """Generate a random state string for CSRF protection."""
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def verify_pkce_challenge(self, client_challenge: str):
        """Verify a PKCE challenge against the stored verifier."""
        if not self._code_verifier:
            raise ValueError("PKCE verifier not set. Call pkce_login() first.")
        expected_challenge = self._generate_code_challenge(self._code_verifier)
        if expected_challenge != client_challenge:
            raise ValueError("Invalid PKCE challenge")

    @staticmethod
    def _generate_code_challenge(verifier: str) -> str:
        """Create SHA-256 hash hex of the SHA-256 of the verifier (Alibaba PKCE spec)."""
        sha256_1 = hashlib.sha256(verifier.encode()).digest()
        sha256_2 = hashlib.sha256(sha256_1).hexdigest()
        return sha256_2

    # ----- OAuth / OIDC protocol helpers ----- #
    def exchange_code_for_token(self, code: str) -> Any:
        """Exchange authorization code for tokens using Alibaba token endpoint."""
        token_url = f"{self.issuer}/oidc/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = urllib.parse.urlencode(
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
            }
        ).encode()
        req = urllib.request.Request(token_url, data, headers)
        # Skip SSL verification for demo; in production validate certificates
        with urllib.request.urlopen(
            req, context=ssl._create_unverified_context()
        ) as resp:
            return resp

    def introspect_token(self, access_token: str) -> Any:
        """Introspect an access token (returns JWT payload)."""
        introspect_url = f"{self.issuer}/oidc/introspect"
        headers = {
            "Authorization": f"Bearer {os.getenv('ALIBABA_IDAAS_CLIENT_SECRET')}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = urllib.parse.urlencode(
            {
                "token": access_token,
                "token_type_hint": "access_token",
            }
        ).encode()
        req = urllib.request.Request(introspect_url, data, headers)
        with urllib.request.urlopen(
            req, context=ssl._create_unverified_context()
        ) as resp:
            return resp

    # ----- Helper for demo token fetch ----- #
    def fetch_demo_token(self) -> Any:
        """Placeholder function to demonstrate token fetch without real flow."""
        # In a real app, use exchange_code_for_token after callback
        return {"access_token": "demo-access-token", "expires_in": 3600}


if __name__ == "__main__":
    client = IdentityClient()
    print("Initialized with issuer:", client.issuer, "client_id:", client.client_id)
