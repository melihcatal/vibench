import os
from identity_client import get_identity_client
from identity_models import UserProfile
from typing import Dict, Any


def fetch_and_normalize_profile_claims(access_token: str) -> Dict[str, Any]:
    identity_client = get_identity_client()

    try:
        userinfo = identity_client.get_userinfo(access_token)

        # Normalize claims into our UserProfile model
        profile = UserProfile(
            sub=userinfo.get("sub"),
            name=userinfo.get("name"),
            given_name=userinfo.get("given_name"),
            family_name=userinfo.get("family_name"),
            nickname=userinfo.get("nickname"),
            preferred_username=userinfo.get("preferred_username"),
            profile=userinfo.get("profile"),
            picture=userinfo.get("picture"),
            website=userinfo.get("website"),
            email=userinfo.get("email"),
            email_verified=userinfo.get("email_verified"),
            gender=userinfo.get("gender"),
            birthdate=userinfo.get("birthdate"),
            zoneinfo=userinfo.get("zoneinfo"),
            locale=userinfo.get("locale"),
            phone_number=userinfo.get("phone_number"),
            phone_number_verified=userinfo.get("phone_number_verified"),
            address=userinfo.get("address"),
            updated_at=userinfo.get("updated_at"),
            custom_claims={k: v for k, v in userinfo.items() if k not in UserProfile.__annotations__}
        )
        return {"status": "success", "profile": profile.__dict__}
    except Exception as e:
        return {"status": "error", "message": str(e)}
