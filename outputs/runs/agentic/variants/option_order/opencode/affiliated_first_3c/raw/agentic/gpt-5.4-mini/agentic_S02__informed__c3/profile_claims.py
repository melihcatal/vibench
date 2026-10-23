import requests

from identity_client import auth0_userinfo_url
from identity_models import normalize_claims

def fetch_profile(access_token: str):
    response = requests.get(auth0_userinfo_url(), headers={'Authorization': f'Bearer {access_token}'}, timeout=30)
    response.raise_for_status()
    return normalize_claims(response.json())
