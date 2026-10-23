import requests
from identity_models import UserProfile, normalize_claims

def fetch_profile_claims(access_token: str) -> UserProfile:
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
    response.raise_for_status()
    raw_claims = response.json()
    return normalize_claims(raw_claims)
