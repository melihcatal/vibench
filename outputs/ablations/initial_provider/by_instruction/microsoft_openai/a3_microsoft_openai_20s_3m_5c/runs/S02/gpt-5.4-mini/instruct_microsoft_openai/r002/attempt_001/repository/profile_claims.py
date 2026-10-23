from typing import Dict

from identity_client import fetch_json
from identity_models import NormalizedProfile, normalize_claims


def fetch_and_normalize_profile(access_token: str) -> NormalizedProfile:
    claims: Dict = fetch_json(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    mapped = {
        "sub": claims.get("id", ""),
        "name": claims.get("displayName", ""),
        "email": claims.get("mail") or claims.get("userPrincipalName", ""),
        "oid": claims.get("id", ""),
        "upn": claims.get("userPrincipalName", ""),
        "raw": claims,
    }
    return normalize_claims(mapped)
