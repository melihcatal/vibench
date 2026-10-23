import requests
from identity_client import Auth0Client
from identity_models import UserInfo, normalize_user_claims

def fetch_and_normalize_profile(access_token: str) -> UserInfo:
    client = Auth0Client()
    userinfo_url = f"https://{client.domain}/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}
    resp = requests.get(userinfo_url, headers=headers)
    resp.raise_for_status()
    raw_claims = resp.json()
    return normalize_user_claims(raw_claims)