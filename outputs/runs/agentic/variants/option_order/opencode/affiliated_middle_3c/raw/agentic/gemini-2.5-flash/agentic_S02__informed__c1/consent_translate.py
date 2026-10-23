import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any


def translate_consent_copy(text: str, target_language: str = "es") -> str:
    """
    Translates identity-provider consent copy using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or the default gcloud credentials.
    # No explicit GOOGLE_APPLICATION_CREDENTIALS check here, as the client handles it.

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return f"Translation Error: {e}"


if __name__ == "__main__":
    english_consent_text = "Do you agree to share your profile information (name, email, picture) with this application?"
    target_lang = "fr"  # French

    print(f"Translating consent copy to {target_lang}: '{english_consent_text}'")
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up (e.g., via gcloud auth application-default login)
    translated_text = translate_consent_copy(english_consent_text, target_lang)
    print("\n--- Translated Consent Copy ---")
    print(translated_text)
