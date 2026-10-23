from auth0.management import Auth0
from identity_client import identity_client
from identity_models import NormalizedProfile


def get_and_normalize_profile(access_token: str) -> NormalizedProfile:
    """
    Fetches user profile from Auth0 /userinfo endpoint and normalizes it.
    """
    config = identity_client.get_auth0_config()

    auth0 = Auth0(config["domain"], access_token)
    userinfo = auth0.users.userinfo(access_token)

    normalized_profile = NormalizedProfile(
        id=userinfo.get("sub"),
        email=userinfo.get("email"),
        name=userinfo.get("name"),
        nickname=userinfo.get("nickname"),
        picture=userinfo.get("picture"),
        raw_claims=userinfo,
    )
    return normalized_profile
