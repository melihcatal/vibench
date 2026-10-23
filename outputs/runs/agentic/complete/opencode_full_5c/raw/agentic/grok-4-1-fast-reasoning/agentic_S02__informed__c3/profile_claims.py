from identity_client import get_auth_config, fetch_user_profile
from identity_models import Tokens, normalize_claims, UserProfile


def fetch_normalized_profile(tokens: Tokens) -> UserProfile:
    config = get_auth_config()
    raw_claims = fetch_user_profile(config, tokens)
    return normalize_claims(raw_claims)
