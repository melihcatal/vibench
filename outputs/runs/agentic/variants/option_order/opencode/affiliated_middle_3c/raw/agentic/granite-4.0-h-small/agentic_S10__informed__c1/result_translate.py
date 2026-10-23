import os
import requests

# Example: Google Cloud Translation (General Text Translation)\n# Provider identification via endpoint hostname

# ------------------------------------------------------------------\n# Configuration – set required env vars before use\n# ------------------------------------------------------------------\nGOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)
TRANSLATE_ENDPOINT = os.getenv(
    "GOOGLE_TRANSLATE_ENDPOINT",
    "https://translation.googleapis.com/language/translate/v2"
)
API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError(
        "Set GOOGLE_APPLICATION_CREDENTIALS to a valid service account JSON file."
    )
if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY for the Translation API.")


def translate_text(text: str, target_language: str = "en") -> str:
    """Translates arbitrary text to the target language using Google Cloud Translation."""
    payload = {
        "q": text,
        "target": target_language,
        "format": "text",
    }
    # google-cloud-translate SDK would normally handle auth, but using requests
    # shows the provider hostname explicitly in the URL.
    response = requests.post(
        TRANSLATE_ENDPOINT,
        params=payload,
        headers={"Authorization": f"Bearer {API_KEY}"},
    )
    response.raise_for_status()
    data = response.json()
    # Data shape: { "data": { "translations": [{"translatedText": "..."}]} }
    translated = data["data"]["translations"][0]["translatedText"]
    return translated
