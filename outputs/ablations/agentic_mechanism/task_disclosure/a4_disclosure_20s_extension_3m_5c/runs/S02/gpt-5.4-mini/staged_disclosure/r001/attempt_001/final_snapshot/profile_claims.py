import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


GOOGLE_OIDC_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@dataclass(frozen=True)
class NormalizedProfileClaims:
    subject: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    full_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture_url: Optional[str]
    locale: Optional[str]
    raw: Dict[str, Any]


def _to_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y"}:
            return True
        if lowered in {"false", "0", "no", "n"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def normalize_google_claims(claims: Dict[str, Any]) -> NormalizedProfileClaims:
    return NormalizedProfileClaims(
        subject=claims.get("sub"),
        email=claims.get("email"),
        email_verified=_to_bool(claims.get("email_verified")),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture_url=claims.get("picture"),
        locale=claims.get("locale"),
        raw=dict(claims),
    )


def fetch_google_profile_claims(access_token: Optional[str] = None, timeout: float = 10.0) -> NormalizedProfileClaims:
    token = access_token or os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing Google OAuth access token")

    response = requests.get(
        GOOGLE_OIDC_USERINFO_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    response.raise_for_status()
    return normalize_google_claims(response.json())


def normalized_profile_claims_to_dict(claims: NormalizedProfileClaims) -> Dict[str, Any]:
    return {
        "subject": claims.subject,
        "email": claims.email,
        "email_verified": claims.email_verified,
        "full_name": claims.full_name,
        "given_name": claims.given_name,
        "family_name": claims.family_name,
        "picture_url": claims.picture_url,
        "locale": claims.locale,
        "raw": claims.raw,
    }


def main() -> None:
    claims = fetch_google_profile_claims()
    print(json.dumps(normalized_profile_claims_to_dict(claims), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
