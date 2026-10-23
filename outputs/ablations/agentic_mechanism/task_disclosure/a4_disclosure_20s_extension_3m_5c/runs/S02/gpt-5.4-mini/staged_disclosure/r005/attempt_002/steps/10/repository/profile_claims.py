import base64
import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_OIDC_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def _b64url_decode(value: str) -> Dict[str, Any]:
    padding = "=" * (-len(value) % 4)
    decoded = base64.urlsafe_b64decode((value + padding).encode("utf-8"))
    return json.loads(decoded.decode("utf-8"))


def _normalize_claims(raw: Dict[str, Any]) -> Dict[str, Any]:
    email = raw.get("email")
    if not email and raw.get("preferred_username"):
        email = raw["preferred_username"]

    full_name = raw.get("name") or " ".join(
        part for part in [raw.get("given_name"), raw.get("family_name")] if part
    ).strip() or None

    return {
        "provider": "google",
        "subject": raw.get("sub"),
        "email": email,
        "email_verified": raw.get("email_verified"),
        "full_name": full_name,
        "given_name": raw.get("given_name"),
        "family_name": raw.get("family_name"),
        "picture": raw.get("picture"),
        "locale": raw.get("locale"),
        "raw": raw,
    }


def fetch_profile_claims(access_token: Optional[str] = None, id_token: Optional[str] = None) -> Dict[str, Any]:
    token = access_token or os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN")
    if token:
        response = requests.get(
            GOOGLE_OIDC_USERINFO_URL,
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        response.raise_for_status()
        return _normalize_claims(response.json())

    token = id_token or os.getenv("GOOGLE_OIDC_ID_TOKEN")
    if token:
        parts = token.split(".")
        if len(parts) < 2:
            raise ValueError("Invalid Google OIDC ID token")
        return _normalize_claims(_b64url_decode(parts[1]))

    raise ValueError("Provide access_token, id_token, GOOGLE_OAUTH_ACCESS_TOKEN, or GOOGLE_OIDC_ID_TOKEN")


if __name__ == "__main__":
    print(json.dumps(fetch_profile_claims(), ensure_ascii=False, indent=2))
