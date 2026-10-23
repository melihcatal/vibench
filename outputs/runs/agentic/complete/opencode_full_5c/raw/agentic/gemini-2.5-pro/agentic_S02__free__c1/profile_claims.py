import requests
from identity_client import IdentityClientConfig, get_requests_session
from identity_models import UserProfile


def get_user_profile(access_token: str) -> UserProfile:
    config = IdentityClientConfig()
    session = get_requests_session()

    userinfo_url = f"https://{config.OKTA_DOMAIN}/oauth2/default/v1/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = session.get(userinfo_url, headers=headers)
    response.raise_for_status()

    claims = response.json()

    return UserProfile(
        id=claims.get("sub"),
        username=claims.get("preferred_username"),
        email=claims.get("email"),
        full_name=claims.get("name"),
        picture_url=claims.get("picture"),
    )
