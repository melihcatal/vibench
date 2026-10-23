import requests
from identity_client import get_okta_oauth_config
from identity_models import UserProfile


def fetch_user_profile(access_token: str):
    """
    Fetches the user profile from the Okta userinfo endpoint.
    """
    okta_config = get_okta_oauth_config()
    userinfo_url = f"{okta_config['issuer']}/v1/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    claims = response.json()

    normalized_profile = UserProfile(
        user_id=claims.get("sub"),
        claims={
            "name": claims.get("name"),
            "email": claims.get("email"),
            "preferred_username": claims.get("preferred_username"),
        },
    )

    return normalized_profile
