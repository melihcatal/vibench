import os
import requests
from typing import Dict, Any
from identity_models import NormalizedProfile

USERINFO_ENDPOINT = "https://graph.microsoft.com/oidc/userinfo"


def fetch_normalized_profile(access_token: str) -> NormalizedProfile:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(USERINFO_ENDPOINT, headers=headers)
    response.raise_for_status()
    claims = response.json()
    
    return NormalizedProfile(
        sub=claims.get("sub"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        email=claims.get("email"),
        picture=claims.get("picture"),
    )