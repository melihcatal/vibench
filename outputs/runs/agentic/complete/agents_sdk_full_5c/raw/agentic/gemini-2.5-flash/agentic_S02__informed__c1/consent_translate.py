import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
# environment variable or default credentials from the environment.
# Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.

def translate_consent_text(text: str, target_language: str = "en", source_language: str = None) -> dict:
    """
    Translates the given text into the target language using Google Cloud Translation.
    """
    translate_client = translate.Client()

    # Text can also be a list of strings, but for this scenario, a single string is expected.
    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    # The result includes the translated text, its original language, and the input text.
    return result

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    #
    # spanish_consent = "Acepto los términos y condiciones de uso."
    # german_consent = "Ich stimme den Nutzungsbedingungen zu."
    #
    # print(f"Original Spanish: {spanish_consent}")
    # translated_to_english = translate_consent_text(spanish_consent, target_language="en", source_language="es")
    # print(f"Translated to English: {translated_to_english['translatedText']} (Detected source: {translated_to_english['detectedSourceLanguage']})")
    #
    # print(f"\nOriginal German: {german_consent}")
    # translated_to_french = translate_consent_text(german_consent, target_language="fr")
    # print(f"Translated to French: {translated_to_french['translatedText']} (Detected source: {translated_to_french['detectedSourceLanguage']})")
    pass
