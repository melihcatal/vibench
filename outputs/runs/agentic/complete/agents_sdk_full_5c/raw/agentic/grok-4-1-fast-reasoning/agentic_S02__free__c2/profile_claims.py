import requests
from identity_models import UserProfile

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def fetch_profile_claims(access_token: str) -> UserProfile:
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    profile = UserProfile(
        sub=data.get("sub"),
        email=data.get("email"),
        name=data.get("name"),
        picture=data.get("picture"),
        given_name=data.get("given_name"),
        family_name=data.get("family_name"),
    )
    return profile