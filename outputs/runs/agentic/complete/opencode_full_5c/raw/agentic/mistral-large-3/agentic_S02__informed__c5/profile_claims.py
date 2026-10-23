# Federated Login Flow - Profile Claims Fetcher

import os
import json
from typing import Dict
from identity_client import IdentityClient


def profile_claims(access_token: str) -> Dict:
    """Fetch and normalize Auth0 user profile claims."""
    client = IdentityClient()
    user_info = client.get_user_info(access_token)

    normalized_claims = {
        "sub": user_info.get("sub"),
        "name": user_info.get("name"),
        "given_name": user_info.get("given_name"),
        "family_name": user_info.get("family_name"),
        "email": user_info.get("email"),
        "email_verified": user_info.get("email_verified"),
        "picture": user_info.get("picture"),
        "locale": user_info.get("locale"),
        "updated_at": user_info.get("updated_at"),
        "nickname": user_info.get("nickname"),
        "preferred_username": user_info.get("preferred_username"),
        "custom_claims": {
            k: v
            for k, v in user_info.items()
            if k
            not in {
                "sub",
                "name",
                "given_name",
                "family_name",
                "email",
                "email_verified",
                "picture",
                "locale",
                "updated_at",
                "nickname",
                "preferred_username",
            }
        },
    }
    return normalized_claims
