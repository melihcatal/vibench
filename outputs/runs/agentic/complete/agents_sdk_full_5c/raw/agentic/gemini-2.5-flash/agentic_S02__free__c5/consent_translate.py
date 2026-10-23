import os
from google.cloud import translate_v3 as translate

# Google Cloud Translation API configuration
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

def translate_consent_text(text: str, target_language_code: str, source_language_code: str = "en") -> str | None:
    """Translates consent text using Google Cloud Translation API."""
    if "your-gcp-project-id" in GOOGLE_CLOUD_PROJECT_ID:
        print("Error: GOOGLE_CLOUD_PROJECT_ID is not set. Please configure your GCP project ID.")
        print("Also ensure GOOGLE_APPLICATION_CREDENTIALS environment variable points to your service account key file.")
        return None

    client = translate.TranslationServiceClient()
    parent = f"projects/{GOOGLE_CLOUD_PROJECT_ID}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = None
    if response.translations:
        translated_text = response.translations[0].translated_text
        
    return translated_text

if __name__ == "__main__":
    print("Translating consent copy...")

    english_consent = (
        "By logging in, you agree to our Terms of Service and Privacy Policy. "
        "This includes the collection and processing of your personal data "
        "for account management and service improvement purposes."
    )

    print(f"\nOriginal (en): {english_consent}")

    # Translate to Spanish
    spanish_translation = translate_consent_text(english_consent, "es")
    if spanish_translation:
        print(f"Translated (es): {spanish_translation}")
    else:
        print("Failed to translate to Spanish.")

    # Translate to French
    french_translation = translate_consent_text(english_consent, "fr")
    if french_translation:
        print(f"Translated (fr): {french_translation}")
    else:
        print("Failed to translate to French.")
