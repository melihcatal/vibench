import os
from google.cloud import translate_v2 as translate

# Configure Google Cloud Translation client
# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
translate_client = translate.Client()

def translate_consent_copy(text: str, target_language: str = "es") -> str:
    """
    Translates identity-provider consent copy using Google Cloud Translation.
    """
    if not text:
        return ""

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        return f"Error translating text with Google Cloud Translation: {e}"

if __name__ == "__main__":
    # Example Usage:
    english_consent = (
        "By clicking 'Accept', you agree to allow this application to access "
        "your basic profile information, including your name and email address. "
        "This information will be used to personalize your experience and is "
        "subject to our privacy policy."
    )

    spanish_consent = translate_consent_copy(english_consent, "es")
    print(f"Original (EN):\n{english_consent}")
    print(f"\nTranslated (ES):\n{spanish_consent}")

    french_consent = translate_consent_copy(english_consent, "fr")
    print(f"\nTranslated (FR):\n{french_consent}")
