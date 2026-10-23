import os
import google.auth.transport.requests
from google.oauth2 import credentials
from googleapiclient.discovery import build

def fetch_and_normalize_profile_claims(access_token: str) -> dict:
    """
    Fetches and normalizes federated user profile claims from Google People API.
    """
    creds = credentials.Credentials(access_token)
    service = build('people', 'v1', credentials=creds)

    # Fetch user profile information
    person = service.people().get(
        resourceName='people/me',
        personFields='emailAddresses,names,photos'
    ).execute()

    # Normalize claims
    normalized_claims = {
        "sub": person.get("resourceName", "").split("/")[-1], # Google's unique ID for the user
        "name": None,
        "email": None,
        "picture": None,
    }

    if "names" in person:
        for name in person["names"]:
            if name.get("metadata", {}).get("primary"):
                normalized_claims["name"] = name.get("displayName")
                break

    if "emailAddresses" in person:
        for email_address in person["emailAddresses"]:
            if email_address.get("metadata", {}).get("primary"):
                normalized_claims["email"] = email_address.get("value")
                break

    if "photos" in person:
        for photo in person["photos"]:
            if photo.get("metadata", {}).get("primary"):
                normalized_claims["picture"] = photo.get("url")
                break

    return normalized_claims
