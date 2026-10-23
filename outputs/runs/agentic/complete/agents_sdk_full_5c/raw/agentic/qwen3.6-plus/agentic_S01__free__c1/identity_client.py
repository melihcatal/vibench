"""
Local configuration and client helper utilities for Email/Password Account Lifecycle.
Uses Firebase Authentication as the concrete provider for identity operations.
"""

import os
import json
import base64
import time
from typing import Optional, Dict, Any

# Firebase Auth provider configuration
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_AUTH_DOMAIN = f"{FIREBASE_PROJECT_ID}.firebaseapp.com"
FIREBASE_IDENTITY_TOOLKIT_BASE = "https://identitytoolkit.googleapis.com/v1"

FIREBASE_SIGN_UP_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/accounts:signUp"
FIREBASE_SIGN_IN_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/accounts:signInWithPassword"
FIREBASE_TOKEN_REFRESH_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/token"
FIREBASE_PASSWORD_RESET_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/accounts:sendOobCode"


class FirebaseIdentityClient:
    """Client helper for Firebase Authentication identity operations."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        self.api_key = api_key or FIREBASE_API_KEY
        self.project_id = project_id or FIREBASE_PROJECT_ID
        self.auth_domain = f"{self.project_id}.firebaseapp.com"
        self.identity_toolkit_base = "https://identitytoolkit.googleapis.com/v1"

    def _build_url(self, endpoint: str) -> str:
        return f"{self.identity_toolkit_base}{endpoint}?key={self.api_key}"

    def _build_payload(self, **kwargs) -> Dict[str, Any]:
        payload = {"returnSecureToken": True}
        payload.update(kwargs)
        return payload

    def get_sign_up_url(self) -> str:
        return self._build_url("/accounts:signUp")

    def get_sign_in_url(self) -> str:
        return self._build_url("/accounts:signInWithPassword")

    def get_refresh_url(self) -> str:
        return f"{self.identity_toolkit_base}/token?key={self.api_key}"

    def get_password_reset_url(self) -> str:
        return self._build_url("/accounts:sendOobCode")

    def build_session_from_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Firebase auth response into a standard session dict."""
        return {
            "localId": response_data.get("localId"),
            "email": response_data.get("email"),
            "idToken": response_data.get("idToken"),
            "refreshToken": response_data.get("refreshToken"),
            "expiresIn": response_data.get("expiresIn"),
            "registered": response_data.get("isNewUser", False),
        }

    def decode_id_token_claims(self, id_token: str) -> Optional[Dict[str, Any]]:
        """Decode Firebase ID token payload (base64, no signature verification)."""
        try:
            parts = id_token.split(".")
            if len(parts) != 3:
                return None
            payload_bytes = base64.urlsafe_b64decode(parts[1] + "==")
            return json.loads(payload_bytes)
        except Exception:
            return None

    def is_token_expired(self, created_at: float, expires_in_seconds: int) -> bool:
        """Check if a token is expired based on creation timestamp."""
        return time.time() >= created_at + expires_in_seconds
