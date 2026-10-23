import json
import os
import requests

# Google Cloud Translation API
TRANSLATE_URL = (
    "https://translation.googleapis.com/v3/projects/{}/locations/{}/translateText"
)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "global"
# Set environment variable GOOGLE_APPLICATION_CREDENTIALS to point to a JSON key file


def translate_vendor_note(note: str, target_lang: str = "es") -> str:
    """Translate a vendor note or memo using Google Cloud Translation."""
    # Build request payload
    payload = {
        "contents": [note],
        "targetLanguageCode": target_lang,
        "sourceLanguageCode": "auto",
    }
    # Fetch the auth credentials from the default path
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    # Add Authorization header
    headers = {"Authorization": f"Bearer {credentials.token}"}
    # Send request
    resp = requests.post(
        TRANSLATE_URL.format(PROJECT_ID, LOCATION), headers=headers, json=payload
    )
    resp.raise_for_status()
    translation = resp.json()["translations"][0]["translatedText"]
    return translation


# Example usage
# print(translate_vendor_note("Invoice total due by 31/12", target_lang='fr'))
