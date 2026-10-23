import requests
from identity_client import GoogleIdentityClient
from identity_models import UserProfile


def fetch_and_normalize_profile(access_token: str) -> UserProfile:
    client = GoogleIdentityClient()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(client.USERINFO_URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    return UserProfile(
        sub=data["sub"],
        email=data.get("email"),
        name=data.get("name"),
        given_name=data.get("given_name"),
        family_name=data.get("family_name"),
        picture=data.get("picture"),
    )
