
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# This is a placeholder for actual Google API credentials.
# In a real application, you would obtain these through an OAuth 2.0 flow.
# For demonstration purposes, we'll assume credentials are set up
# (e.g., from environment variables or a loaded JSON file).
# Replace with your actual client ID, client secret, and redirect URI.
def get_mock_google_credentials():
    # In a real scenario, you'd load credentials from a secure source
    # and refresh them as needed. This is a simplified mock.
    # Ensure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN are set in your environment
    return Credentials(
        token=None,  # Token will be refreshed if using a refresh token
        refresh_token=os.environ.get("GOOGLE_REFRESH_TOKEN", "YOUR_REFRESH_TOKEN"),
        client_id=os.environ.get("GOOGLE_CLIENT_ID", "YOUR_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]
    )

def get_google_people_service(credentials):
    """Builds and returns a Google People API service object."""
    try:
        service = build("people", "v1", credentials=credentials)
        return service
    except HttpError as error:
        print(f"An error occurred while building Google People API service: {error}")
        return None

def fetch_google_profile_claims(service):
    """Fetches user profile claims using the Google People API."""
    try:
        profile = service.people().get(
            resourceName="people/me",
            personFields="names,emailAddresses,photos,birthdays,genders,locales"
        ).execute()
        return profile
    except HttpError as error:
        print(f"An error occurred while fetching Google profile: {error}")
        return None

def normalize_claims(raw_claims):
    """Normalizes raw claims from Google People API into a standard format."""
    normalized = {}

    # Example of normalizing name
    if "names" in raw_claims and raw_claims["names"]:
        primary_name = raw_claims["names"][0]
        normalized["first_name"] = primary_name.get("givenName")
        normalized["last_name"] = primary_name.get("familyName")
        normalized["full_name"] = primary_name.get("displayName")

    # Example of normalizing email
    if "emailAddresses" in raw_claims and raw_claims["emailAddresses"]:
        primary_email = raw_claims["emailAddresses"][0]
        normalized["email"] = primary_email.get("value")

    # Example of normalizing photo
    if "photos" in raw_claims and raw_claims["photos"]:
        primary_photo = raw_claims["photos"][0]
        normalized["picture"] = primary_photo.get("url")

    # Example of normalizing gender
    if "genders" in raw_claims and raw_claims["genders"]:
        primary_gender = raw_claims["genders"][0]
        normalized["gender"] = primary_gender.get("value")

    # Example of normalizing birthday
    if "birthdays" in raw_claims and raw_claims["birthdays"]:
        primary_birthday = raw_claims["birthdays"][0].get("date")
        if primary_birthday:
            normalized["birthday"] = f"{primary_birthday.get("year")}-{primary_birthday.get("month")}-{primary_birthday.get("day")}"

    # Example of normalizing locale
    if "locales" in raw_claims and raw_claims["locales"]:
        primary_locale = raw_claims["locales"][0]
        normalized["locale"] = primary_locale.get("value")

    return normalized

if __name__ == "__main__":
    print("Attempting to fetch and normalize Google profile claims...")

    # For a real application, ensure your environment variables are set:
    # GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN
    # Or implement a proper OAuth flow to get credentials.
    credentials = get_mock_google_credentials()

    if credentials:
        service = get_google_people_service(credentials)
        if service:
            raw_claims = fetch_google_profile_claims(service)
            if raw_claims:
                normalized_claims = normalize_claims(raw_claims)
                print("\nRaw Google Profile Claims:")
                print(raw_claims)
                print("\nNormalized Profile Claims:")
                print(normalized_claims)
            else:
                print("Failed to fetch raw Google profile claims.")
        else:
            print("Failed to initialize Google People API service.")
    else:
        print("Failed to get Google API credentials. Please set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN environment variables, or implement a proper OAuth flow.")
