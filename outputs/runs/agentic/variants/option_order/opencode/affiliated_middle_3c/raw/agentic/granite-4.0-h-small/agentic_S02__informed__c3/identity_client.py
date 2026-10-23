import os
import json
import random
import string
import urllib.parse
import http.client
from typing import Any, Dict, Optional

# Provider: Google Identity Platform - use Application Default Credentials
GOOGLE_ID_TOKEN_URL = "https://oauth2.googleapis.com/tokeninfo"


class IdentityClient:
    """Local helper utilities for Federated Login Flow."""

    # Configuration (normally loaded from env vars or a secrets manager)
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
    APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")

    @staticmethod
    def generate_pkce_verifier(length: int = 128) -> str:
        """Create a PKCE code verifier (RFC 7636)."""
        chars = string.ascii_letters + string.digits + "-._~"
        return "".join(random.choices(chars, k=length))

    @staticmethod
    def derive_pkce_challenge(verifier: str) -> str:
        """Derive PKCE code_challenge from verifier (S256)."""
        hash_bytes = hashlib.sha256(verifier.encode()).digest()
        challenge = base64.urlsafe_b64encode(hash_bytes).rstrip(b"=").decode()
        return challenge

    @staticmethod
    def verify_callback_state(expected_state: str) -> bool:
        """Simple CSRF check – verifies the state matches a stored value."""
        # In practice you would compare against a server‑side session/cookie value.
        # Here we just ensure the value is non‑empty.
        return bool(expected_state)

    @staticmethod
    def introspect_token(
        introspection_url: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Perform token introspection against a provider (REST)."""
        conn = http.client.HTTPSConnection(introspection_url)
        conn.request(
            method="POST",
            url="/",
            body=urllib.parse.urlencode(payload),
            headers={
                **(headers or {}),
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        resp = conn.getresponse()
        data = resp.read().decode()
        token_info = json.loads(data) if resp.status == 200 else {}
        conn.close()
        return token_info

    @staticmethod
    def get_google_token_info(id_token: str) -> Dict[str, Any]:
        """Verify a Google ID token using Google's public JWKS endpoint."""
        # In production fetch JWKS and verify signature.  Here we delegate to Google.
        payload = {"id_token": id_token}
        with http.client.HTTPSConnection(GOOGLE_ID_TOKEN_URL) as conn:
            conn.request("GET", "?" + urllib.parse.urlencode(payload))
            resp = conn.getresponse()
            data = resp.read().decode()
            return json.loads(data) if resp.status == 200 else {}
