# HELPER: identity_models.py
# Local request, response, and normalization helpers for Federated Login Flow

from __future__ import annotations
from typing import Any, Dict, Optional, List


# Normalized claim model
class NormalizedClaims:
    def __init__(self, data: Dict[str, Any]):
        self.user_id: Optional[str] = data.get("user_id")
        self.full_name: Optional[str] = data.get("full_name")
        self.email: Optional[str] = data.get("email")
        self.email_verified: Optional[bool] = data.get("email_verified")
        self.extra: Dict[str, Any] = {
            k: v
            for k, v in data.items()
            if k not in ["user_id", "full_name", "email", "email_verified"]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "email_verified": self.email_verified,
            **self.extra,
        }


# Raw response model (as received from provider)
class RawProviderResponse:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw

    def to_dict(self) -> Dict[str, Any]:
        return self.raw


# Helper to map provider raw data to normalized model
def map_to_normalized(raw_claims: Dict[str, Any]) -> NormalizedClaims:
    # Example mapping for Auth0 (can be extended for other providers)
    normalized = {
        "user_id": raw_claims.get("sub"),
        "full_name": raw_claims.get("name"),
        "email": raw_claims.get("email"),
        "email_verified": raw_claims.get("email_verified"),
    }
    return NormalizedClaims(normalized)


# Example: validate email verification


def is_email_verified(raw_claims: Dict[str, Any]) -> bool:
    return raw_claims.get("email_verified", False)


# Example: compose request payload for token exchange (PKCE)
class TokenExchangeRequest:
    def __init__(self, code: str, verifier: str, redirect_uri: str = None):
        self.code = code
        self.verifier = verifier
        self.redirect_uri = redirect_uri or "http://localhost:3000/oauth_callback"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "grant_type": "authorization_code",
            "code": self.code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.verifier,
        }


# Simple test harness
if __name__ == "__main__":
    # Dummy raw payload (replace with actual provider response)
    dummy_raw = {
        "sub": "auth0|123456",
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "email_verified": True,
        "nickname": "jane",
    }
    norm = map_to_normalized(dummy_raw)
    print("Normalized claims:", norm.to_dict())
