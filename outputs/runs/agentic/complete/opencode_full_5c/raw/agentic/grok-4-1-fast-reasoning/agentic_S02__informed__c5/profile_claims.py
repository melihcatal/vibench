from identity_client import IdentityClient
from identity_models import UserProfile


def fetch_and_normalize_claims(access_token: str) -> UserProfile:
    client = IdentityClient()
    raw_profile = client.get_user_profile(access_token)
    # Normalize claims
    normalized = UserProfile(
        sub=raw_profile.sub,
        email=raw_profile.email or None,
        name=raw_profile.name or None,
        picture=raw_profile.picture or None,
    )
    return normalized


if __name__ == "__main__":
    # Example usage placeholder
    pass
