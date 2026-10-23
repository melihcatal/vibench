from typing import Dict, Optional
import requests
from identity_models import ProfileClaims

# Google People API with concrete model identifier
PROVIDER_NAME = "google"
USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"
PEOPLE_API_ENDPOINT = "https://people.googleapis.com/v1/people/me"
MODEL_ID = "google-people-api-v1"


def fetch_profile_claims(access_token: str) -> ProfileClaims:
    """Fetch and normalize user profile claims from Google's People API."""
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

    # Fetch basic profile from UserInfo endpoint
    userinfo_response = requests.get(USERINFO_ENDPOINT, headers=headers)
    userinfo_response.raise_for_status()
    userinfo_data = userinfo_response.json()

    # Fetch extended profile from People API
    people_response = requests.get(
        PEOPLE_API_ENDPOINT,
        headers=headers,
        params={"personFields": "names,emailAddresses,photos,metadata"},
    )
    people_response.raise_for_status()
    people_data = people_response.json()

    # Normalize claims
    return ProfileClaims(
        sub=userinfo_data.get("sub"),
        name=people_data.get("names", [{}])[0].get("displayName")
        if people_data.get("names")
        else userinfo_data.get("name"),
        given_name=people_data.get("names", [{}])[0].get("givenName")
        if people_data.get("names")
        else None,
        family_name=people_data.get("names", [{}])[0].get("familyName")
        if people_data.get("names")
        else None,
        email=userinfo_data.get("email"),
        email_verified=userinfo_data.get("email_verified", False),
        picture=people_data.get("photos", [{}])[0].get("url")
        if people_data.get("photos")
        else userinfo_data.get("picture"),
        locale=userinfo_data.get("locale"),
        provider=PROVIDER_NAME,
        model_id=MODEL_ID,
    )
