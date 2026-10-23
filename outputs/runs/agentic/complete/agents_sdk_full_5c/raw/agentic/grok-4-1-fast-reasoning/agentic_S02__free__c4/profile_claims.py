import requests
from identity_client import GoogleOAuthConfig
from identity_models import UserProfile, normalize_profile

def fetch_profile_claims(access_token: str) -> UserProfile:
    config = GoogleOAuthConfig()
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(config.USERINFO_URL, headers=headers)
    response.raise_for_status()
    raw_claims = response.json()
    return normalize_profile(raw_claims)