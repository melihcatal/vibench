import requests
from identity_models import UserProfile

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def fetch_profile_claims(access_token: str) -> UserProfile:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    response.raise_for_status()
    claims = response.json()
    return UserProfile(
        sub=claims["sub"],
        email=claims.get("email"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
    )
