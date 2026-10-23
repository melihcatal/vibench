from identity_client import get_cognito_oauth_config, get_user_info
from identity_models import UserProfileClaims


def fetch_and_normalize_profile_claims(access_token: str) -> UserProfileClaims:
    config = get_cognito_oauth_config()
    user_profile = get_user_info(access_token, config)
    return user_profile
