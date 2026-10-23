import os
import requests
from identity_client import get_config
from identity_models import UserProfile, normalize_profile

def fetch_profile_claims(access_token: str) -> UserProfile:
    tenant_id = os.getenv('AZURE_TENANT_ID')
    config = get_config()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    response = requests.get(config['userinfo_endpoint'], headers=headers)
    response.raise_for_status()
    claims = response.json()
    return normalize_profile(claims)