import requests
from identity_client import get_okta_config
from identity_models import UserProfile


def get_user_profile(access_token: str) -> UserProfile:
    """
    Fetches user profile claims from Okta's userinfo endpoint.
    """
    config = get_okta_config()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(config.userinfo_endpoint, headers=headers)
    response.raise_for_status()

    claims = response.json()

    return UserProfile(
        sub=claims.get("sub"),
        name=claims.get("name"),
        email=claims.get("email"),
        raw_claims=claims,
    )
