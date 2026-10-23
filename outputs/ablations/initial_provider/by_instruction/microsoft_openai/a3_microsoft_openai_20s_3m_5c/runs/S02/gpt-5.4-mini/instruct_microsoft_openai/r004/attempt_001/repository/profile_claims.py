import requests

from identity_client import microsoft_userinfo_url
from identity_models import UserClaims, normalize_claims


def fetch_profile_claims(access_token: str) -> UserClaims:
    response = requests.get(microsoft_userinfo_url(), headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    response.raise_for_status()
    return normalize_claims(response.json(), provider="microsoft")
