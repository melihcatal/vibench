import os
import requests
import jwt

from identity_client import get_auth0_domain
from identity_models import UserProfileClaims


def fetch_and_normalize_profile_claims(
    access_token: str, id_token: str
) -> UserProfileClaims:
    """Fetches and normalizes federated user profile claims from Auth0."""
    auth0_domain = get_auth0_domain()

    # Decode ID token for basic claims
    decoded_id_token = jwt.decode(
        id_token, options={"verify_signature": False}
    )  # In production, verify signature

    # Use access token to get more profile info from Userinfo endpoint
    userinfo_url = f"https://{auth0_domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    userinfo_claims = response.json()

    # Normalize claims
    normalized_claims = UserProfileClaims(
        sub=decoded_id_token.get("sub"),
        name=userinfo_claims.get("name", decoded_id_token.get("name")),
        email=userinfo_claims.get("email", decoded_id_token.get("email")),
        picture=userinfo_claims.get("picture", decoded_id_token.get("picture")),
        preferred_username=userinfo_claims.get(
            "nickname", decoded_id_token.get("preferred_username")
        ),
        given_name=userinfo_claims.get("given_name"),
        family_name=userinfo_claims.get("family_name"),
        locale=userinfo_claims.get("locale"),
        # Add other claims as needed
    )
    return normalized_claims
