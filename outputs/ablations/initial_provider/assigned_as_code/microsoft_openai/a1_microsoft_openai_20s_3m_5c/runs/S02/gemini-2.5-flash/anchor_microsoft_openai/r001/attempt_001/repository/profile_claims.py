import requests
from identity_client import get_auth0_config
from identity_models import UserProfile

def fetch_and_normalize_profile_claims(access_token: str) -> UserProfile:
    auth0_config = get_auth0_config()
    domain = auth0_config["DOMAIN"]
    
    userinfo_url = f"https://{domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize claims
    user_profile = UserProfile(
        user_id=claims.get("sub") or claims.get("user_id"),
        email=claims.get("email"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        updated_at=claims.get("updated_at"),
        raw_claims=claims
    )
    return user_profile
