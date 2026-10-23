from identity_client import MicrosoftEntraIdentityClient
from identity_models import UserProfileClaims


def fetch_profile_claims(access_token: str) -> UserProfileClaims:
    client = MicrosoftEntraIdentityClient()
    user_info = client.get_user_info(access_token)

    return UserProfileClaims(
        sub=user_info.get("sub"),
        name=user_info.get("name"),
        given_name=user_info.get("given_name"),
        family_name=user_info.get("family_name"),
        email=user_info.get("email"),
        email_verified=user_info.get("email_verified"),
        picture=user_info.get("picture"),
        locale=user_info.get("locale"),
        preferred_username=user_info.get("preferred_username"),
    )
