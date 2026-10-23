import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    or authenticated using `gcloud auth application-default login`.
    """
    translate_client = translate.Client()

    # Target can be a language code or a language name.
    # target_language = 'fr'

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    # The translated text is returned as a dictionary, extract the 'translatedText' field.
    translated_text = result['translatedText']
    return translated_text

if __name__ == 'main':
    # Example usage:
    # consent_text = "By clicking 'Accept', you agree to our Terms and Conditions."
    # target_lang = "es"
    # try:
    #     translated_consent = translate_consent_copy(consent_text, target_lang)
    #     print(f"Original ({os.environ.get('SOURCE_LANG', 'en')}): {consent_text}")
    #     print(f"Translated ({target_lang}): {translated_consent}")
    # except Exception as e:
    #     print(f"Error translating consent copy: {e}")
    #     print("Ensure GOOGLE_APPLICATION_CREDENTIALS is set or gcloud is authenticated.")
    pass
