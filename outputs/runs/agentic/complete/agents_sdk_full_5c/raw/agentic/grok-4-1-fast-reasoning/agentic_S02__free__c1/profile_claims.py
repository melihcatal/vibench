import requests
from identity_client import GOOGLE_USERINFO_URL
from identity_models import UserClaims, normalize_claims

def fetch_profile_claims(access_token: str) -> UserClaims:
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'FederatedLogin/1.0'
    }
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    response.raise_for_status()
    raw_claims = response.json()
    return normalize_claims(raw_claims)
