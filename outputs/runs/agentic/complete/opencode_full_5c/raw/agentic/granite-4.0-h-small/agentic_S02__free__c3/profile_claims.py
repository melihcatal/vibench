# profile_claims.py
# SAME-SCENARIO: Fetches and normalizes federated user profile claims from the identity token (Google OIDC)

import json
from typing import Dict, Any

from identity_client import IdentityClient  # local helper

# Define a normalized claim schema that all providers should map to
NormalizedClaims = Dict[str, Any]


def normalize_google_claims(token: dict) -> NormalizedClaims:
    """
    Convert raw Google OIDC token payload into a consistent internal claim shape.

    Expected raw fields (Google's id_token payload):
    - sub
    - email
    - email_verified
    - name
    - given_name
    - family_name
    - picture
    - locale
    """
    normalized = {
        "user_id": token.get("sub"),
        "email": token.get("email"),
        "email_verified": token.get("email_verified"),
        "full_name": token.get("name"),
        "given_name": token.get("given_name"),
        "family_name": token.get("family_name"),
        "picture_url": token.get("picture"),
        "locale": token.get("locale"),
        # Keep raw Google claims for audit if needed
        "_raw_google": token,
    }
    return normalized


def fetch_claims(id_token: str) -> NormalizedClaims:
    """
    Verify the JWT signature (via local library) and extract raw claims.

    In production you would use a JWT library like python-jose or PyJWT.
    Here we use IdentityClient as a placeholder for a provider SDK that offers
    a verify_id_token method.
    """
    client = IdentityClient()
    # provider‑specific verification; SDK returns raw claims dict
    raw_claims = client.verify_google_id_token(id_token)
    return normalize_google_claims(raw_claims)


# Example usage (e.g., called from oauth_callback after token exchange)
if __name__ == "__main__":
    fake_id_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    claims = fetch_claims(fake_id_token)
    print("Normalized user claims:", json.dumps(claims, indent=2))
