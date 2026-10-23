from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


MICROSOFT_GRAPH_ME_ENDPOINT = "https://graph.microsoft.com/v1.0/me"


@dataclass
class ProfileClaims:
    subject: str
    email: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    display_name: Optional[str]
    locale: Optional[str]
    raw: Dict[str, Any]


def _pick_email(payload: Dict[str, Any]) -> Optional[str]:
    for key in ("mail", "userPrincipalName", "preferred_username", "email"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _pick_subject(payload: Dict[str, Any]) -> str:
    for key in ("id", "sub", "oid"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    email = _pick_email(payload)
    if email:
        return email
    raise ValueError("Unable to determine subject from Microsoft Graph profile")


def normalize_profile_claims(payload: Dict[str, Any]) -> ProfileClaims:
    return ProfileClaims(
        subject=_pick_subject(payload),
        email=_pick_email(payload),
        given_name=payload.get("givenName") if isinstance(payload.get("givenName"), str) else None,
        family_name=payload.get("surname") if isinstance(payload.get("surname"), str) else None,
        display_name=payload.get("displayName") if isinstance(payload.get("displayName"), str) else None,
        locale=payload.get("preferredLanguage") if isinstance(payload.get("preferredLanguage"), str) else None,
        raw=payload,
    )


def fetch_profile_claims(access_token: str, session: Optional[requests.Session] = None) -> ProfileClaims:
    client = session or requests.Session()
    response = client.get(
        MICROSOFT_GRAPH_ME_ENDPOINT,
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Microsoft Graph profile response must be an object")
    return normalize_profile_claims(payload)
