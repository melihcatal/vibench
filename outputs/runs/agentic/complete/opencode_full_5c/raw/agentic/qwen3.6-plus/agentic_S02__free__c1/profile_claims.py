import os
from typing import Optional, Dict, Any, List

from identity_models import UserProfile, normalize_google_claims
from identity_client import fetch_userinfo


GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_PEOPLE_API_URL = "https://people.googleapis.com/v1/people/me"


def fetch_google_profile_claims(
    access_token: str,
    include_people_api: bool = False,
    google_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    import requests

    userinfo = fetch_userinfo(
        _build_google_config(),
        access_token,
    )

    profile = normalize_google_claims(userinfo)

    additional_data = {}
    if include_people_api and google_api_key:
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get(
            GOOGLE_PEOPLE_API_URL,
            headers=headers,
            params={
                "personFields": "names,emailAddresses,photos,locales",
                "key": google_api_key,
            },
            timeout=30,
        )
        if resp.status_code == 200:
            additional_data = resp.json()

    return {
        "profile": profile.to_dict(),
        "additional_data": additional_data,
        "provider": "google",
        "userinfo_endpoint": GOOGLE_USERINFO_URL,
    }


def fetch_google_profile_from_id_token(
    id_token: str,
) -> Dict[str, Any]:
    import requests

    resp = requests.get(
        GOOGLE_TOKENINFO_URL,
        params={"id_token": id_token},
        timeout=30,
    )
    resp.raise_for_status()
    token_info = resp.json()

    profile = normalize_google_claims(token_info)

    return {
        "profile": profile.to_dict(),
        "token_info": token_info,
        "provider": "google",
        "tokeninfo_endpoint": GOOGLE_TOKENINFO_URL,
    }


def normalize_google_profile(profile: UserProfile) -> Dict[str, Any]:
    return {
        "federated_id": profile.sub,
        "email": profile.email,
        "email_verified": profile.email_verified,
        "display_name": profile.name,
        "first_name": profile.given_name,
        "last_name": profile.family_name,
        "avatar_url": profile.picture,
        "locale": profile.locale,
        "idp": "google",
        "raw_claims": profile.raw_claims,
    }


def extract_google_group_memberships(
    access_token: str,
    customer_id: str = "my_customer",
) -> List[str]:
    import requests

    resp = requests.get(
        "https://admin.googleapis.com/admin/directory/v1/groups",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"customer": customer_id, "userKey": "me"},
        timeout=30,
    )
    if resp.status_code != 200:
        return []
    data = resp.json()
    return [g.get("email", "") for g in data.get("groups", [])]


def _build_google_config():
    from identity_models import OAuthConfig

    return OAuthConfig(
        provider="google",
        client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        redirect_uri=os.environ.get(
            "GOOGLE_REDIRECT_URI", "http://localhost:3000/callback"
        ),
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        token_url="https://oauth2.googleapis.com/token",
        userinfo_url=GOOGLE_USERINFO_URL,
        scopes=["openid", "profile", "email"],
    )
