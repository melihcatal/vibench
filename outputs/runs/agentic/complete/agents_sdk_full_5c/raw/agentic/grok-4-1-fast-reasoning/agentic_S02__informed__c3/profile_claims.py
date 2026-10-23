import requests
from identity_client import USERINFO_URL
from identity_models import UserProfile, normalize_profile

def fetch_profile_claims(access_token: str) -> UserProfile:
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(USERINFO_URL, headers=headers)
    resp.raise_for_status()
    profile = resp.json()
    return normalize_profile(profile)