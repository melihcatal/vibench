from identity_client import get_identity_client
from identity_models import UserProfile


def get_user_profile(access_token: str) -> UserProfile:
    client = get_identity_client()

    userinfo = client.auth0.userinfo(access_token)

    return UserProfile(
        user_id=userinfo.get("sub"),
        name=userinfo.get("name"),
        email=userinfo.get("email"),
        raw_claims=userinfo,
    )
