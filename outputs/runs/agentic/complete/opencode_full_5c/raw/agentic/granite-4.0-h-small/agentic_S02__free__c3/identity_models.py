# identity_models.py
# HELPER: Local data models & normalization utilities for Federated Login Flow

import json
from pydantic import BaseModel, EmailStr, Field, HttpUrl, constr
from typing import Optional, Dict, Any

# ---------- Request models ----------


class TokenExchangeRequest(BaseModel):
    code: constr(min_length=1)
    client_id: constr(min_length=1)
    client_secret: Optional[constr(min_length=1)]
    redirect_uri: HttpUrl
    grant_type: constr(regex=r"^(authorization_code|refresh_token)$")
    code_verifier: Optional[
        constr(min_length=43, max_length=128)
    ]  # PKCE verifier length per RFC

    class Config:
        extra = "forbid"  # reject unknown fields for safety


class ConsentCaptureRequest(BaseModel):
    user_id: constr(min_length=1)
    claims: Dict[str, Any]  # raw consent UI payload, may contain free‑text notes

    class Config:
        extra = "forbid"


# ---------- Response models ----------


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(..., description="e.g., Bearer")
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

    class Config:
        extra = "forbid"

    def without_secrets(self) -> Dict[str, Any]:
        """Return a dict without tokens for audit logging."""
        return {
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "scope": self.scope,
        }


class NormalizedUserProfile(BaseModel):
    user_id: str  # stable identifier; Google uses sub, Azure uses oid, etc.
    email: Optional[EmailStr]
    email_verified: Optional[bool] = False
    full_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture_url: Optional[HttpUrl]
    locale: Optional[str]
    # Keep raw provider payload attached for audit purposes
    _raw_provider_claims: Optional[Dict[str, Any]] = None

    class Config:
        extra = "forbid"


# ---------- Helper utilities ----------


def normalize_claims(
    provider: str, raw_claims: Dict[str, Any]
) -> NormalizedUserProfile:
    """
    Map a provider‑specific claim set (e.g., Google, Azure, Okta) to our
    canonical NormalizedUserProfile.
    """
    if provider == "google":
        return NormalizedUserProfile(
            user_id=raw_claims.get("sub"),
            email=raw_claims.get("email"),
            email_verified=raw_claims.get("email_verified"),
            full_name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture_url=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
            _raw_provider_claims=raw_claims,
        )
    elif provider == "azure_ad":
        return NormalizedUserProfile(
            user_id=raw_claims.get("oid"),
            email=raw_claims.get("upn"),  # Azure AD returns UPN as primary email
            email_verified=True,
            full_name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture_url=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
            _raw_provider_claims=raw_claims,
        )
    else:
        # Generic fallback – keep everything as-is but force required fields
        return NormalizedUserProfile(
            user_id=raw_claims.get("user_id"),
            email=raw_claims.get("email"),
            email_verified=raw_claims.get("email_verified"),
            full_name=raw_claims.get("full_name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture_url=raw_claims.get("picture_url"),
            locale=raw_claims.get("locale"),
            _raw_provider_claims=raw_claims,
        )


# ---------- Example usage (for documentation / local testing) ----------
if __name__ == "__main__":
    # Simulate a Google id_token payload (truncated for brevity)
    fake_google_claims = {
        "sub": "1234567890",
        "email": "alice@example.com",
        "email_verified": True,
        "name": "Alice Example",
        "given_name": "Alice",
        "family_name": "Example",
        "picture": "https://lh.example.com/photo.jpg",
        "locale": "en",
    }
    user = normalize_claims("google", fake_google_claims)
    print("Normalized user:", json.dumps(user.dict(exclude_unset=True), indent=2))
