import requests
import jwt
from typing import Dict, Any
from identity_client import get_auth0_config
from identity_models import UserProfile


def fetch_user_profile_claims(access_token: str) -> UserProfile:
    config = get_auth0_config()
    if not config.domain:
        raise ValueError("Auth0 domain not configured.")

    # Auth0 userinfo endpoint
    userinfo_url = f"https://{config.domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize claims
    return UserProfile(
        sub=claims.get("sub", ""),
        name=claims.get("name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        picture=claims.get("picture"),
        raw_claims=claims,
    )


def decode_id_token(id_token: str) -> UserProfile:
    # Note: For production, proper ID token validation (signature, expiry, etc.) is crucial.
    # This is a simplified decode for demonstration.
    decoded_claims: Dict[str, Any] = jwt.decode(
        id_token, options={"verify_signature": False}
    )

    return UserProfile(
        sub=decoded_claims.get("sub", ""),
        name=decoded_claims.get("name"),
        email=decoded_claims.get("email"),
        email_verified=decoded_claims.get("email_verified"),
        picture=decoded_claims.get("picture"),
        raw_claims=decoded_claims,
    )
