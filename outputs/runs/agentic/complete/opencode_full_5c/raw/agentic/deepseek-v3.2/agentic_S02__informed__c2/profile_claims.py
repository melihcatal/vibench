import os
import requests
import json
import jwt
from identity_client import IdentityClient
from identity_models import UserProfile, NormalizedClaims


def fetch_user_profile(access_token):
    """Fetch and normalize federated user profile claims."""
    client = IdentityClient()

    # Auth0 specific userinfo endpoint
    auth0_domain = os.environ.get("AUTH0_DOMAIN")

    if not auth0_domain:
        raise ValueError("AUTH0_DOMAIN environment variable must be set")

    userinfo_url = f"https://{auth0_domain}/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        # Fetch user profile from Auth0
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        userinfo = response.json()

        # Parse Auth0 userinfo response
        profile = UserProfile(
            sub=userinfo.get("sub"),
            email=userinfo.get("email"),
            email_verified=userinfo.get("email_verified"),
            name=userinfo.get("name"),
            given_name=userinfo.get("given_name"),
            family_name=userinfo.get("family_name"),
            nickname=userinfo.get("nickname"),
            picture=userinfo.get("picture"),
            locale=userinfo.get("locale"),
            updated_at=userinfo.get("updated_at"),
        )

        # Normalize claims to standard format
        normalized = NormalizedClaims(
            user_id=profile.sub,
            email=profile.email,
            email_verified=profile.email_verified,
            full_name=profile.name,
            first_name=profile.given_name,
            last_name=profile.family_name,
            display_name=profile.nickname or profile.name,
            avatar_url=profile.picture,
            locale=profile.locale,
            provider="auth0",
            raw_claims=userinfo,
        )

        return normalized

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch user profile: {str(e)}")


def validate_id_token(id_token, nonce):
    """Validate ID token and extract claims."""
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not auth0_domain or not auth0_client_id:
        raise ValueError("Auth0 environment variables must be set")

    # Get Auth0 JWKS for token validation
    jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"

    try:
        jwks_response = requests.get(jwks_url)
        jwks_response.raise_for_status()
        jwks = jwks_response.json()

        # Decode and validate ID token
        decoded = jwt.decode(
            id_token,
            jwks,
            algorithms=["RS256"],
            audience=auth0_client_id,
            issuer=f"https://{auth0_domain}/",
            options={"verify_nonce": True},
        )

        # Verify nonce
        if decoded.get("nonce") != nonce:
            raise ValueError("Invalid nonce in ID token")

        return decoded

    except (jwt.InvalidTokenError, requests.exceptions.RequestException) as e:
        raise ValueError(f"ID token validation failed: {str(e)}")
