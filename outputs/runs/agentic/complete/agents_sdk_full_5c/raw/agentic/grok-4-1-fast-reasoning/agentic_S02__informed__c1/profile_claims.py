import os
import requests
from typing import Optional
from identity_models import UserClaims

def fetch_and_normalize_profile(access_token: str) -> UserClaims:
    domain = os.getenv('AUTH0_DOMAIN')
    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable not set")
    userinfo_endpoint = f"https://{domain}/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(userinfo_endpoint, headers=headers)
    response.raise_for_status()
    raw_claims = response.json()
    normalized = UserClaims(
        sub=raw_claims['sub'],
        email=raw_claims.get('email'),
        name=raw_claims.get('name'),
        email_verified=raw_claims.get('email_verified'),
        picture=raw_claims.get('picture')
    )
    return normalized
