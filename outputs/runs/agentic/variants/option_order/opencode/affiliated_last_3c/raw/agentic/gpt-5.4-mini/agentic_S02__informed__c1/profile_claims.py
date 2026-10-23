from typing import Dict

from identity_client import fetch_userinfo
from identity_models import normalize_claims


def get_normalized_profile(access_token: str) -> Dict[str, object]:
    claims = fetch_userinfo(access_token)
    return normalize_claims(claims)
