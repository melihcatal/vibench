import requests
import msal
from identity_client import get_config
from identity_models import normalize_profile, UserProfile

config = get_config()

def fetch_and_normalize_profile(access_token: str) -> UserProfile:
    app = msal.PublicClientApplication(config["client_id"], authority=config["authority"])
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(
        config["userinfo_endpoint"],
        headers=headers
    )
    response.raise_for_status()
    claims = response.json()
    return normalize_profile(claims)

# Provider-specific: msal, https://login.microsoftonline.com/.../v2.0/userinfo endpoint