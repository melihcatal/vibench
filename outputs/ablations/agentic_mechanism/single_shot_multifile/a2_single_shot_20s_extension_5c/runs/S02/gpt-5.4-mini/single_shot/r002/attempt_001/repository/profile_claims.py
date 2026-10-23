import os
from typing import Any

import requests

from identity_client import get_oauth_config, get_userinfo
from identity_models import ProfileClaims, normalize_profile_claims

OIDC_USERINFO_URL = os.getenv("OIDC_USERINFO_URL", "https://YOUR_PROVIDER.example.com/oauth2/v3/userinfo")


def fetch_profile_claims(access_token: str) -> dict[str, Any]:
    config = get_oauth_config()
    claims = get_userinfo(userinfo_endpoint=OIDC_USERINFO_URL, access_token=access_token, issuer=config.issuer)
    normalized = normalize_profile_claims(ProfileClaims.from_dict(claims))
    return normalized.to_dict()
