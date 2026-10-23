from typing import Any, Dict

from identity_client import fetch_userinfo, load_config
from identity_models import normalize_claims


def fetch_profile_claims(access_token: str) -> Dict[str, Any]:
    config = load_config()
    claims = fetch_userinfo(access_token)
    claims["issuer"] = config.issuer
    return normalize_claims(claims)
