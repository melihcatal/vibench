import os
import requests
from identity_client import USERINFO_ENDPOINT
from identity_models import UserProfileClaims

def fetch_google_user_profile(access_token: str) -> UserProfileClaims:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(USERINFO_ENDPOINT, headers=headers)
    response.raise_for_status()
    
    return UserProfileClaims(response.json())
