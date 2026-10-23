import os
from google.cloud import translate_v2 as translate

# Configure Google Cloud Translation
# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment or passed implicitly.


def translate_consent_copy(text: str, target_language: str = "en") -> str:
    """
    Translates identity-provider consent copy using Google Cloud Translation.
    Args:
        text: The consent text to translate.
        target_language: The ISO 639-1 code of the target language (e.g., "en", "es", "fr").
    Returns:
        The translated text.
    """
    try:
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        return f"Error translating consent copy with Google Cloud Translation: {e}"


if __name__ == "__main__":
    sample_consent_text = (
        "Je consens à partager mes informations de profil avec cette application."
    )
    translated_text = translate_consent_copy(sample_consent_text, target_language="en")
    print(f"Original (French): {sample_consent_text}")
    print(f"Translated (English): {translated_text}")

    spanish_consent_text = (
        "I consent to share my profile information with this application."
    )
    translated_spanish = translate_consent_copy(
        spanish_consent_text, target_language="es"
    )
    print(f"Original (English): {spanish_consent_text}")
    print(f"Translated (Spanish): {translated_spanish}")
