from typing import Any, Dict, Optional

import requests
from jose import jwt

from identity_client import get_identity_provider_config
from identity_models import FederatedProfile

AUTH0_USERINFO_URL = "https://{domain}/userinfo"


def fetch_and_normalize_profile(access_token: str, id_token: Optional[str] = None) -> FederatedProfile:
    config = get_identity_provider_config()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(AUTH0_USERINFO_URL.format(domain=config.provider_domain), headers=headers, timeout=15)
    response.raise_for_status()
    claims: Dict[str, Any] = response.json()
    if id_token:
        claims["id_token"] = id_token
        try:
            claims["jwt_subject"] = jwt.get_unverified_claims(id_token).get("sub")
        except Exception:
            claims["jwt_subject"] = None
    return FederatedProfile.from_claims(claims)
