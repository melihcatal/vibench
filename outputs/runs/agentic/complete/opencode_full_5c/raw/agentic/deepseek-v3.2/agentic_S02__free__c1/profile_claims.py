import requests
from identity_models import UserProfile, NormalizedProfile
from identity_client import get_userinfo_endpoint


def fetch_user_profile(access_token, provider="google"):
    """Fetch user profile claims from provider's userinfo endpoint."""
    userinfo_endpoint = get_userinfo_endpoint(provider)

    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

    response = requests.get(userinfo_endpoint, headers=headers)
    response.raise_for_status()

    claims = response.json()

    if provider == "google":
        return UserProfile(
            sub=claims["sub"],
            email=claims.get("email"),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            provider=provider,
            raw_claims=claims,
        )

    elif provider == "microsoft":
        return UserProfile(
            sub=claims.get("sub") or claims.get("oid"),
            email=claims.get("email") or claims.get("preferred_username"),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("surname"),
            picture=None,
            locale=None,
            provider=provider,
            raw_claims=claims,
        )

    elif provider == "github":
        return UserProfile(
            sub=str(claims["id"]),
            email=claims.get("email"),
            email_verified=claims.get("verified", False),
            name=claims.get("name"),
            given_name=None,
            family_name=None,
            picture=claims.get("avatar_url"),
            locale=None,
            provider=provider,
            raw_claims=claims,
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def normalize_profile(profile):
    """Normalize user profile claims to a standard format."""
    normalized = NormalizedProfile(
        user_id=profile.sub,
        email=profile.email,
        email_verified=profile.email_verified,
        full_name=profile.name,
        first_name=profile.given_name,
        last_name=profile.family_name,
        avatar_url=profile.picture,
        locale=profile.locale,
        provider=profile.provider,
        original_profile=profile,
    )

    if profile.provider == "github" and not normalized.email:
        normalized.email = fetch_github_primary_email(
            profile.raw_claims.get("access_token")
        )

    return normalized


def fetch_github_primary_email(access_token):
    """Fetch primary email from GitHub (requires additional scope)."""
    if not access_token:
        return None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get("https://api.github.com/user/emails", headers=headers)
    response.raise_for_status()

    emails = response.json()
    for email in emails:
        if email.get("primary") and email.get("verified"):
            return email["email"]

    return None


def validate_profile_claims(profile, required_claims=None):
    """Validate that profile contains required claims."""
    if required_claims is None:
        required_claims = ["sub", "email"]

    missing = []
    for claim in required_claims:
        if not getattr(profile, claim, None):
            missing.append(claim)

    if missing:
        raise ValueError(f"Missing required claims: {missing}")

    return True
