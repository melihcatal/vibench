import os
import requests
from typing import Dict

# Microsoft identity platform (Microsoft Entra ID)
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

def fetch_normalized_profile(access_token: str) -> Dict:
    userinfo_url = f"https://graph.microsoft.com/oidc/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()
    
    normalized = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "preferred_username": claims.get("preferred_username"),
        "provider": "microsoft_entra_id",
    }
    return normalized