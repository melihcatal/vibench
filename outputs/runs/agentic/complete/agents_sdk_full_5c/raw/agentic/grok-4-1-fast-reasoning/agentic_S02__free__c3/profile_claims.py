import requests
from .identity_models import UserProfile, normalize_profile

def fetch_profile_claims(access_token: str) -&gt; UserProfile:
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(
        'https://openidconnect.googleapis.com/v1/userinfo',
        headers=headers
    )
    response.raise_for_status()
    claims = response.json()
    return normalize_profile(claims)
