import requests
from typing import Dict, Any
from .identity_models import UserClaims, normalize_claims


def fetch_and_normalize_profile(access_token: str) -> UserClaims:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo", headers=headers
    )
    response.raise_for_status()
    raw_claims: Dict[str, Any] = response.json()
    return normalize_claims(raw_claims)
