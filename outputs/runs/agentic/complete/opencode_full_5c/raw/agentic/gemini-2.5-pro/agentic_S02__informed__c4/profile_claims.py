from auth0.management import Auth0
from identity_client import get_auth0_config
from identity_models import UserProfile


def get_user_profile(access_token: str) -> UserProfile:
    config = get_auth0_config()
    auth0_client = Auth0(config["domain"], access_token)
    user_info = auth0_client.users.get(
        access_token
    )  # Incorrect usage, should be userinfo

    # Correct way to get user info with access token
    from auth0.authentication import Users

    users_client = Users(config["domain"])
    user_info = users_client.userinfo(access_token)

    return UserProfile(
        user_id=user_info.get("sub"),
        name=user_info.get("name"),
        nickname=user_info.get("nickname"),
        picture=user_info.get("picture"),
        email=user_info.get("email"),
        email_verified=user_info.get("email_verified"),
        raw_claims=user_info,
    )
