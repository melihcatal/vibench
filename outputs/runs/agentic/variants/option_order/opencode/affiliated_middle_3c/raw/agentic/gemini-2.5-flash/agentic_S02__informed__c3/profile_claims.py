import requests

from identity_client import get_auth0_userinfo_url
from identity_models import UserProfile


def fetch_and_normalize_profile_claims(access_token: str) -> UserProfile:
    """Fetches and normalizes federated user profile claims from Auth0.

    Args:
        access_token: The access token obtained during the OAuth flow.

    Returns:
        A UserProfile object containing normalized user claims.

    Raises:
        Exception: If fetching user info fails.
    """
    userinfo_url = get_auth0_userinfo_url()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    return UserProfile(
        sub=claims["sub"],
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        picture=claims.get("picture"),
        federated_claims=claims,
    )
