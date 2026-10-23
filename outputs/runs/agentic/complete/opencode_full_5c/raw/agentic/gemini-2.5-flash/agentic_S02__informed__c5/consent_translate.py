import os
from google.cloud import translate_v2 as translate


def translate_consent_copy(
    text: str, target_language: str = "es", source_language: str = "en"
) -> dict:
    """Translates identity-provider consent copy using Google Cloud Translation.

    Args:
        text: The consent copy to translate.
        target_language: The language to translate to (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English). Default is "en".

    Returns:
        A dictionary containing the translated text and detected source language.
    """
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # Ensure this environment variable points to your service account key file.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text, target_language=target_language, source_language=source_language
        )
        return {
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "input_text": text,
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Example Usage:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/google-cloud-key.json"

    english_consent = (
        "By clicking 'Accept', you agree to our Terms of Service and Privacy Policy. "
        "This allows us to process your personal data for providing services."
    )

    print("Translating English consent to Spanish:")
    print(translate_consent_copy(english_consent, target_language="es"))

    french_consent = (
        "En cliquant sur 'Accepter', vous acceptez nos Conditions d'utilisation et notre Politique de confidentialité. "
        "Cela nous permet de traiter vos données personnelles pour la fourniture de services."
    )

    print("\nTranslating French consent to English (auto-detect source):")
    print(translate_consent_copy(french_consent, target_language="en"))
