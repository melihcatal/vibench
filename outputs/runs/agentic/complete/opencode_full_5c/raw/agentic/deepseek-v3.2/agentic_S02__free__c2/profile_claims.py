import requests
from typing import Dict, Any, Optional
from identity_client import IdentityClient
from identity_models import ProfileRequest, NormalizedProfile


def fetch_profile_claims(request: ProfileRequest) -> NormalizedProfile:
    client = IdentityClient()

    if request.id_token:
        claims = client.decode_id_token(request.id_token)
    elif request.access_token:
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {request.access_token}"}
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        claims = response.json()
    else:
        raise ValueError("Either id_token or access_token is required")

    return normalize_google_profile(claims)


def normalize_google_profile(claims: Dict[str, Any]) -> NormalizedProfile:
    email = claims.get("email", "")
    email_verified = claims.get("email_verified", False)

    return NormalizedProfile(
        subject=claims.get("sub", ""),
        email=email,
        email_verified=email_verified,
        name=claims.get("name", ""),
        given_name=claims.get("given_name", ""),
        family_name=claims.get("family_name", ""),
        picture=claims.get("picture", ""),
        locale=claims.get("locale", ""),
        provider="google",
        raw_claims=claims,
    )
