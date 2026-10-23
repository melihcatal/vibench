import os
from google.cloud import translate_v3 as translate
from typing import List

# Google Cloud Translation API
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set

def translate_consent_copy(text_to_translate: str, target_language_code: str, project_id: str) -> str:
    """Translates identity-provider consent copy using Google Cloud Translation API.

    Args:
        text_to_translate: The text content of the consent copy.
        target_language_code: The ISO 639-1 language code of the target language (e.g., "es", "fr").
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == "__main__":
    # Replace with your actual Google Cloud Project ID
    GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

    if GOOGLE_CLOUD_PROJECT_ID == "your-gcp-project-id":
        print("WARNING: Please set GOOGLE_CLOUD_PROJECT_ID environment variable with your GCP project ID.")
        print("Also, ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key file.")
    
    english_consent_copy = (
        "By clicking 'Accept', you agree to our Terms of Service and Privacy Policy. "
        "This includes the collection and processing of your personal data as described therein."
    )

    print("\n--- Translating Consent Copy to Spanish ---")
    spanish_translation = translate_consent_copy(
        english_consent_copy, "es", GOOGLE_CLOUD_PROJECT_ID
    )
    print(f"Original (EN): {english_consent_copy}")
    print(f"Translated (ES): {spanish_translation}")

    print("\n--- Translating Consent Copy to French ---")
    french_translation = translate_consent_copy(
        english_consent_copy, "fr", GOOGLE_CLOUD_PROJECT_ID
    )
    print(f"Original (EN): {english_consent_copy}")
    print(f"Translated (FR): {french_translation}")

    print("\n--- Translating empty text ---")
    empty_translation = translate_consent_copy(
        "", "de", GOOGLE_CLOUD_PROJECT_ID
    )
    print(f"Translated empty text (DE): '{empty_translation}'")
