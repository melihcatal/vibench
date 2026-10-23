import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from identity_models import UserProfileClaims

def fetch_and_normalize_profile_claims(credentials: Credentials) -> UserProfileClaims:
    """
    Fetches user profile claims using the Google People API and normalizes them.
    """
    service = build("people", "v1", credentials=credentials)
    profile = service.people().get(resourceName="people/me", personFields="emailAddresses,names,photos").execute()

    email = None
    if "emailAddresses" in profile:
        for email_address in profile["emailAddresses"]:
            if email_address.get("metadata", {}).get("primary"): # type: ignore
                email = email_address["value"]
                break
        if not email and profile["emailAddresses"]:
            email = profile["emailAddresses"][0]["value"]

    name = None
    if "names" in profile:
        for person_name in profile["names"]:
            if person_name.get("metadata", {}).get("primary"): # type: ignore
                name = person_name["displayName"]
                break
        if not name and profile["names"]:
            name = profile["names"][0]["displayName"]

    picture = None
    if "photos" in profile:
        for photo in profile["photos"]:
            if photo.get("metadata", {}).get("primary"): # type: ignore
                picture = photo["url"]
                break
        if not picture and profile["photos"]:
            picture = profile["photos"][0]["url"]

    claims = UserProfileClaims(
        sub=credentials.id_token_jwt['sub'] if credentials.id_token_jwt else 'unknown',
        email=email,
        name=name,
        picture=picture,
        raw_profile=profile
    )

    print("Fetched and normalized profile claims:")
    print(f"  Subject: {claims.sub}")
    print(f"  Email: {claims.email}")
    print(f"  Name: {claims.name}")
    print(f"  Picture: {claims.picture}")

    return claims
