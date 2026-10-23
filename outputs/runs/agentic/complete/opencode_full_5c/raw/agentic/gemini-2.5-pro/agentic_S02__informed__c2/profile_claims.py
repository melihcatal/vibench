import os
from auth0.authentication import Users
from identity_models import NormalizedProfile


def get_and_normalize_profile(access_token: str) -> NormalizedProfile:
    domain = os.environ.get("AUTH0_DOMAIN")

    users_client = Users(domain)
    user_info = users_client.userinfo(access_token)

    normalized_profile = NormalizedProfile(
        id=user_info.get("sub"),
        nickname=user_info.get("nickname"),
        name=user_info.get("name"),
        email=user_info.get("email"),
        email_verified=user_info.get("email_verified", False),
        picture=user_info.get("picture"),
        created_at=user_info.get(
            "updated_at"
        ),  # Auth0 often uses updated_at for creation
        updated_at=user_info.get("updated_at"),
        raw_claims=user_info,
    )

    return normalized_profile


if __name__ == "__main__":
    # This is not part of the library, just for demonstration
    # In a real flow, you get the access_token after the OAuth callback.
    print("This script requires a valid access token to run.")
