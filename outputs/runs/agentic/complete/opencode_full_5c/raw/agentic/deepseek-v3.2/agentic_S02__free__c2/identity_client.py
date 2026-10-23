import os
import json
import time
import jwt
import requests
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class IdentityClient:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        self.redirect_base = os.getenv("REDIRECT_BASE_URI", "http://localhost:8000")
        self.state_store = {}

    def build_authorization_url(
        self, state: str, nonce: Optional[str], scopes: list, redirect_uri: str
    ) -> str:
        scope_str = " ".join(scopes)
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": scope_str,
            "redirect_uri": redirect_uri,
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }
        if nonce:
            params["nonce"] = nonce

        return f"https://accounts.google.com/o/oauth2/v2/auth?{self._encode_params(params)}"

    def store_state(self, state: str, data: Dict[str, Any]):
        self.state_store[state] = {"data": data, "timestamp": time.time()}

    def get_state(self, state: str) -> Optional[Dict[str, Any]]:
        if state in self.state_store:
            stored = self.state_store[state]
            if time.time() - stored["timestamp"] < 300:
                return stored["data"]
            del self.state_store[state]
        return None

    def validate_id_token(self, id_token: str, expected_nonce: Optional[str] = None):
        jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
        jwks_response = requests.get(jwks_url)
        jwks = jwks_response.json()

        try:
            decoded = jwt.decode(
                id_token,
                jwks,
                algorithms=["RS256"],
                audience=self.client_id,
                options={"verify_exp": True},
            )

            if expected_nonce and decoded.get("nonce") != expected_nonce:
                raise ValueError("Nonce mismatch")

            return decoded
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid ID token: {e}")

    def decode_id_token(self, id_token: str) -> Dict[str, Any]:
        return jwt.decode(id_token, options={"verify_signature": False})

    def _encode_params(self, params: Dict[str, Any]) -> str:
        import urllib.parse

        return urllib.parse.urlencode(params)
