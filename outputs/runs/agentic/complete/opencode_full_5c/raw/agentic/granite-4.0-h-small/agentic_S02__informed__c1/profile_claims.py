import json
from typing import Any, Dict
from identity_models import ProfileClaim
from identity_client import IdentityClient


def normalize_profile_claims(id_token: str) -> ProfileClaim:
    """Decode and normalize Google ID token payload into a standardized ProfileClaim.

    The ID token is a JWT with a registered claims set + custom profile claims.
    This function validates basic structure, extracts fields, and maps them to
    the consistent structure defined in identity_models.ProfileClaim.
    """
    try:
        header, payload_b64, signature = id_token.split(".")
        payload = json.loads(_b64_decode(payload_b64))
    except Exception as exc:
        raise ValueError("Invalid JWT format for ID token") from exc

    # Map known claims to standardized fields
    claim_map = {
        "sub": "user_id",
        "email": "email",
        "email_verified": "email_verified",
        "name": "full_name",
        "given_name": "given_name",
        "family_name": "family_name",
        "picture": "avatar_url",
        "locale": "locale",
    }
    claim_data: Dict[str, Any] = {}
    for key, mapped in claim_map.items():
        if key in payload:
            claim_data[mapped] = payload[key]
    # Default values for omitted optional fields
    claim_data.setdefault("email_verified", False)
    claim_data.setdefault("locale", "en-US")
    return ProfileClaim(**claim_data)


# Helper to decode base64url without padding


def _b64_decode(b64url: str) -> str:
    # Add padding if missing
    rem = len(b64url) % 4
    if rem:
        b64url += "=" * (4 - rem)
    return b64url.replace("-", "+").replace("_", "/")


# Example usage (called after successful token exchange)
# token_resp = exchange_code_for_tokens(...)
# profile = normalize_profile_claims(token_resp.id_token)
# print(profile.dict())
