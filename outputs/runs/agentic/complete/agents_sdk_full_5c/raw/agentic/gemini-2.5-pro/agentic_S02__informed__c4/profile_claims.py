from auth0.authentication import Users
from identity_client import get_auth0_config
from identity_models import NormalizedProfile

def fetch_and_normalize_profile(access_token: str) -> NormalizedProfile:
    """
    Fetches user profile information from the Auth0 /userinfo endpoint
    and normalizes it into a standard format.

    Args:
        access_token: The access token obtained during the login flow.

    Returns:
        A NormalizedProfile object.
    """
    config = get_auth0_config()
    auth0_users = Users(config["domain"])

    user_info = auth0_users.userinfo(access_token)

    # Normalize the claims from the provider-specific format
    normalized = NormalizedProfile(
        id=user_info.get("sub"),
        name=user_info.get("name"),
        email=user_info.get("email"),
        email_verified=user_info.get("email_verified", False),
        picture=user_info.get("picture"),
        raw_claims=user_info,
    )
    return normalized

# Example usage:
# access_token = session['user_tokens']['access_token']
# profile = fetch_and_normalize_profile(access_token)
# print(f"Welcome, {profile.name}!")
