import os
from google.cloud import translate_v2 as translate

# Using Google Cloud Translation for consent copy translation
# Provider: Google Cloud Translation
# Identifiable signal: google-cloud-translate SDK import, translate.Client(), GOOGLE_APPLICATION_CREDENTIALS (implicitly via SDK)

def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> dict:
    """
    Translates identity-provider consent copy using Google Cloud Translation.

    Args:
        text: The text string to be translated.
        target_language: The ISO-639-1 language code of the target language (e.g., 'es', 'fr').
        source_language: Optional. The ISO-639-1 language code of the source language.
                         If not provided, Google Cloud Translation will attempt to detect it.

    Returns:
        A dictionary containing the translation result, including the translated text,
        detected source language, and model used.
        Example: {'translatedText': 'Hola Mundo', 'detectedSourceLanguage': 'en', 'model': 'nmt'}
    """
    # Google Cloud Translation client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard Google Cloud authentication mechanisms.
    # Ensure your environment is configured with appropriate credentials (e.g., `gcloud auth application-default login`)
    # or by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # No explicit API key needed if using Application Default Credentials.

    translate_client = translate.Client()

    try:
        if source_language:
            result = translate_client.translate(text, target_language=target_language, source_language=source_language)
        else:
            result = translate_client.translate(text, target_language=target_language)

        return result
    except Exception as e:
        print(f"Error translating consent copy with Google Cloud Translation: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    # Ensure your Google Cloud authentication is set up (e.g., `gcloud auth application-default login`)

    print("--- Translating Consent Copy ---")

    consent_english = (
        "By clicking 'Agree', you consent to the processing of your personal data"
        " as described in our Privacy Policy and Terms of Service."
    )
    print(f"\nOriginal (English): {consent_english}")

    print("\nTranslating to Spanish...")
    spanish_translation = translate_consent_copy(consent_english, target_language='es')
    print(f"Translated (Spanish): {spanish_translation.get('translatedText')}")
    print(f"Detected Source Language: {spanish_translation.get('detectedSourceLanguage')}")

    print("\nTranslating to French (explicit source language)...")
    french_translation = translate_consent_copy(consent_english, target_language='fr', source_language='en')
    print(f"Translated (French): {french_translation.get('translatedText')}")
    print(f"Detected Source Language: {french_translation.get('detectedSourceLanguage')}")

    consent_german = "Durch Klicken auf \'Zustimmen\' stimmen Sie der Verarbeitung Ihrer persönlichen Daten gemäß unserer Datenschutzrichtlinie und Nutzungsbedingungen zu."
    print(f"\nOriginal (German): {consent_german}")

    print("\nTranslating German to English...")
    english_from_german = translate_consent_copy(consent_german, target_language='en')
    print(f"Translated (English): {english_from_german.get('translatedText')}")
    print(f"Detected Source Language: {english_from_german.get('detectedSourceLanguage')}")
