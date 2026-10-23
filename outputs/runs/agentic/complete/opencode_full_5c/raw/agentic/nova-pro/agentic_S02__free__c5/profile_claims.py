import identity_client
import identity_models


def fetch_profile(access_token: str) -> identity_models.UserProfile:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(identity_client.USERINFO_URL, headers=headers)
    profile = response.json()
    return identity_models.UserProfile(
        sub=profile["sub"], name=profile["name"], email=profile["email"]
    )
