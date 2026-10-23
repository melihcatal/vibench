import time
from identity_models import OAuthConfig, UserProfile, NormalizedClaims
from identity_client import load_oauth_config, fetch_user_info, normalize_claims


def fetch_profile_claims(
    access_token: str,
    config: OAuthConfig | None = None,
    provider: str = "auth0",
) -> dict:
    if config is None:
        config = load_oauth_config()

    profile: UserProfile = fetch_user_info(
        config=config,
        access_token=access_token,
    )

    normalized: NormalizedClaims = normalize_claims(profile, provider=provider)

    return {
        "user_id": normalized.user_id,
        "email": normalized.email,
        "email_verified": normalized.email_verified,
        "display_name": normalized.display_name,
        "first_name": normalized.first_name,
        "last_name": normalized.last_name,
        "avatar_url": normalized.avatar_url,
        "locale": normalized.locale,
        "provider": normalized.provider,
        "provider_user_id": normalized.provider_user_id,
        "federated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "extra_attributes": normalized.extra_attributes,
        "raw_claims": profile.raw_claims,
    }


def get_normalized_claims(
    access_token: str,
    config: OAuthConfig | None = None,
) -> NormalizedClaims:
    if config is None:
        config = load_oauth_config()
    profile = fetch_user_info(config=config, access_token=access_token)
    return normalize_claims(profile, provider="auth0")


if __name__ == "__main__":
    import os

    token = os.getenv("AUTH0_ACCESS_TOKEN", "")
    if token:
        claims = fetch_profile_claims(access_token=token)
        print(f"User: {claims['display_name']}")
        print(f"Email: {claims['email']}")
        print(f"Provider: {claims['provider']}")
