"""
Fetch and normalize federated user profile claims from Auth0.

Provider: Auth0 Authentication API (UserInfo endpoint)
Environment variables: AUTH0_DOMAIN, AUTH0_CLIENT_ID

Calls the Auth0 /userinfo endpoint with the access token
and normalizes the returned claims into a standard UserProfile format.
"""

from __future__ import annotations

from typing import Optional

import requests

from identity_client import Auth0Config
from identity_models import ClaimNormalizer, UserProfile


class Auth0ProfileFetcher:
    """Fetches and normalizes user profile claims from Auth0."""

    def __init__(self, config: Optional[Auth0Config] = None):
        self.config = config or Auth0Config()

    def fetch_profile(self, access_token: str) -> UserProfile:
        """
        Fetch user profile claims from the Auth0 UserInfo endpoint.

        Args:
            access_token: The OIDC access token obtained from token exchange.

        Returns:
            A normalized UserProfile object.
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        response = requests.get(
            self.config.userinfo_endpoint,
            headers=headers,
            timeout=30,
        )

        if response.status_code != 200:
            raise Auth0ProfileFetchError(
                f"Failed to fetch profile from Auth0: {response.status_code}",
                status_code=response.status_code,
            )

        raw_claims = response.json()
        return ClaimNormalizer.normalize(raw_claims)

    def fetch_profile_with_app_metadata(
        self, access_token: str
    ) -> tuple[UserProfile, dict]:
        """
        Fetch profile and extract app_metadata and user_metadata from claims.

        Auth0 can include app_metadata and user_metadata in the ID token
        or return them via the Management API. This method extracts them
        if present in the userinfo response.
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        response = requests.get(
            self.config.userinfo_endpoint,
            headers=headers,
            timeout=30,
        )

        if response.status_code != 200:
            raise Auth0ProfileFetchError(
                f"Failed to fetch profile from Auth0: {response.status_code}",
                status_code=response.status_code,
            )

        raw_claims = response.json()
        app_metadata = raw_claims.get("app_metadata", {})
        user_metadata = raw_claims.get("user_metadata", {})

        metadata = {
            "app_metadata": app_metadata,
            "user_metadata": user_metadata,
        }

        profile = ClaimNormalizer.normalize(raw_claims)
        return profile, metadata


class Auth0ProfileFetchError(Exception):
    """Raised when fetching profile from Auth0 fails."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def fetch_profile_claims(
    access_token: str,
    config: Optional[Auth0Config] = None,
) -> UserProfile:
    """
    Convenience function to fetch and normalize user profile claims from Auth0.

    Returns a normalized UserProfile.
    """
    fetcher = Auth0ProfileFetcher(config=config)
    return fetcher.fetch_profile(access_token)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python profile_claims.py <access_token>")
        sys.exit(1)

    token = sys.argv[1]

    try:
        profile = fetch_profile_claims(token)
        print(f"Subject: {profile.subject}")
        print(f"Email: {profile.email}")
        print(f"Name: {profile.name}")
        print(f"Provider: {profile.provider}")
    except Auth0ProfileFetchError as e:
        print(f"Error: {e}")
